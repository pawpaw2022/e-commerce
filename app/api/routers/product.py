from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal
from ...db.database import db

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

# Product creation model
class ProductCreate(BaseModel):
    productName: str = Field(..., min_length=1, max_length=100)
    categoryId: int
    price: Decimal = Field(..., gt=0, decimal_places=2)

@router.post("/", status_code=201)
def create_product(product: ProductCreate):
    try:
        # First verify if category exists
        category_query = "SELECT categoryId FROM Categories WHERE categoryId = %s"
        category = db.execute_single(category_query, (product.categoryId,))
        
        if not category:
            raise HTTPException(
                status_code=400,
                detail=f"Category with ID {product.categoryId} does not exist"
            )
        
        # Get the maximum product ID
        max_id_query = "SELECT COALESCE(MAX(productId), 0) as max_id FROM Products"
        max_id_result = db.execute_single(max_id_query)
        new_product_id = max_id_result['max_id'] + 1
        
        # Insert the product with the new ID
        insert_query = """
            INSERT INTO Products (
                productId,
                productName,
                categoryId,
                price
            ) VALUES (%s, %s, %s, %s)
        """
        
        params = (
            new_product_id,
            product.productName,
            product.categoryId,
            float(product.price)  # Convert Decimal to float for MySQL
        )
        
        try:
            db.execute_write(insert_query, params)
            
            # Fetch the created product
            new_product = db.execute_single(
                "SELECT * FROM Products WHERE productId = %s",
                (new_product_id,)
            )
            
            return {"message": "Product created successfully", "product": new_product}
            
        except Exception as e:
            if "foreign key constraint fails" in str(e).lower():
                raise HTTPException(
                    status_code=400,
                    detail="Invalid category ID"
                )
            raise
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_products(
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    product_name: Optional[str] = None
):
    try:
        query = "SELECT * FROM Products WHERE 1=1"
        params = []
        
        if category_id:
            query += " AND categoryId = %s"
            params.append(category_id)
        
        if min_price is not None:
            query += " AND price >= %s"
            params.append(min_price)
            
        if max_price is not None:
            query += " AND price <= %s"
            params.append(max_price)
            
        if product_name:
            query += " AND productName LIKE %s"
            params.append(f"%{product_name}%")
            
        query += " ORDER BY productId ASC"
            
        results = db.execute_many(query, params)
        return {"products": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}")
def get_product_by_id(product_id: int):
    try:
        query = "SELECT * FROM Products WHERE productId = %s"
        result = db.execute_single(query, (product_id,))
        
        if not result:
            raise HTTPException(status_code=404, detail="Product not found")
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{product_id}", status_code=200)
def delete_product(product_id: int):
    try:
        # First check if product exists
        check_query = "SELECT productId FROM Products WHERE productId = %s"
        product = db.execute_single(check_query, (product_id,))
        
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID {product_id} not found"
            )
        
        # Delete related reviews first
        delete_reviews_query = "DELETE FROM Reviews WHERE productId = %s"
        db.execute_write(delete_reviews_query, (product_id,))
        
        # Delete related orders
        delete_orders_query = "DELETE FROM Orders WHERE productId = %s"
        db.execute_write(delete_orders_query, (product_id,))
        
        # Delete the product
        delete_query = "DELETE FROM Products WHERE productId = %s"
        rows_affected = db.execute_write(delete_query, (product_id,))
        
        if rows_affected == 0:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete product"
            )
            
        return {
            "message": "Product and related orders/reviews deleted successfully",
            "product_id": product_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 