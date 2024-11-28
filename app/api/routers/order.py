from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from ...db.database import db

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

class OrderCreate(BaseModel):
    customerId: int
    productId: int
    quantity: int = Field(..., gt=0)

@router.post("/", status_code=201)
def create_order(order: OrderCreate):
    try:
        # Verify if customer exists
        customer_query = "SELECT customerId FROM Customers WHERE customerId = %s"
        customer = db.execute_single(customer_query, (order.customerId,))
        if not customer:
            raise HTTPException(status_code=400, detail="Customer not found")
            
        # Verify if product exists
        product_query = "SELECT productId FROM Products WHERE productId = %s"
        product = db.execute_single(product_query, (order.productId,))
        if not product:
            raise HTTPException(status_code=400, detail="Product not found")
        
        # Get the maximum order ID
        max_id_query = "SELECT COALESCE(MAX(orderId), 0) as max_id FROM Orders"
        max_id_result = db.execute_single(max_id_query)
        new_order_id = max_id_result['max_id'] + 1
        
        # Insert the order
        insert_query = """
            INSERT INTO Orders (
                orderId,
                customerId,
                productId,
                orderDate,
                quantity
            ) VALUES (%s, %s, %s, CURDATE(), %s)
        """
        
        params = (
            new_order_id,
            order.customerId,
            order.productId,
            order.quantity
        )
        
        db.execute_write(insert_query, params)
        
        # Fetch the created order
        new_order = db.execute_single(
            "SELECT * FROM Orders WHERE orderId = %s",
            (new_order_id,)
        )
        
        return {"message": "Order created successfully", "order": new_order}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_orders(
    customer_id: Optional[int] = None,
    product_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    try:
        query = "SELECT * FROM Orders WHERE 1=1"
        params = []
        
        if customer_id:
            query += " AND customerId = %s"
            params.append(customer_id)
            
        if product_id:
            query += " AND productId = %s"
            params.append(product_id)
            
        if start_date:
            query += " AND orderDate >= %s"
            params.append(start_date)
            
        if end_date:
            query += " AND orderDate <= %s"
            params.append(end_date)
            
        query += " ORDER BY orderId ASC"
        
        results = db.execute_many(query, params)
        return {"orders": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{order_id}")
def get_order(order_id: int):
    try:
        query = "SELECT * FROM Orders WHERE orderId = %s"
        result = db.execute_single(query, (order_id,))
        
        if not result:
            raise HTTPException(status_code=404, detail="Order not found")
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{order_id}", status_code=200)
def delete_order(order_id: int):
    try:
        # Check if order exists
        check_query = "SELECT orderId FROM Orders WHERE orderId = %s"
        order = db.execute_single(check_query, (order_id,))
        
        if not order:
            raise HTTPException(
                status_code=404,
                detail=f"Order with ID {order_id} not found"
            )
        
        # Delete the order
        delete_query = "DELETE FROM Orders WHERE orderId = %s"
        rows_affected = db.execute_write(delete_query, (order_id,))
        
        if rows_affected == 0:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete order"
            )
            
        return {
            "message": "Order deleted successfully",
            "order_id": order_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 