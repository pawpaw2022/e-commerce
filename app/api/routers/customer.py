from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional
from ...db.database import db

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

# Customer model for creation and updates
class CustomerCreate(BaseModel):
    firstName: str = Field(..., min_length=1, max_length=50)
    lastName: str = Field(..., min_length=1, max_length=50)
    addressState: str = Field(..., min_length=2, max_length=50)

# Add this model class after CustomerCreate
class CustomerUpdate(BaseModel):
    firstName: Optional[str] = Field(None, min_length=1, max_length=50)
    lastName: Optional[str] = Field(None, min_length=1, max_length=50)
    addressState: Optional[str] = Field(None, min_length=2, max_length=50)

@router.post("/", status_code=201)
def create_customer(customer: CustomerCreate):
    try:
        # Get the maximum customer ID
        max_id_query = "SELECT COALESCE(MAX(customerId), 0) as max_id FROM Customers"
        max_id_result = db.execute_single(max_id_query)
        new_customer_id = max_id_result['max_id'] + 1
        
        # Insert the customer with the new ID
        insert_query = """
            INSERT INTO Customers (
                customerId,
                firstName,
                lastName,
                addressState
            ) VALUES (%s, %s, %s, %s)
        """
        
        params = (
            new_customer_id,
            customer.firstName,
            customer.lastName,
            customer.addressState
        )
        
        try:
            db.execute_write(insert_query, params)
            
            # Fetch the created customer
            new_customer = db.execute_single(
                "SELECT * FROM Customers WHERE customerId = %s",
                (new_customer_id,)
            )
            
            return {"message": "Customer created successfully", "customer": new_customer}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_customers(
    state: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
):
    try:
        query = "SELECT * FROM Customers WHERE 1=1"
        params = []
        
        if state:
            query += " AND addressState = %s"
            params.append(state)
            
        if first_name:
            query += " AND firstName LIKE %s"
            params.append(f"%{first_name}%")
            
        if last_name:
            query += " AND lastName LIKE %s"
            params.append(f"%{last_name}%")
            
        query += " ORDER BY customerId ASC"
        
        results = db.execute_many(query, params)
        return {"customers": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{customer_id}")
def get_customer(customer_id: int):
    try:
        query = "SELECT * FROM Customers WHERE customerId = %s"
        result = db.execute_single(query, (customer_id,))
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{customer_id}", status_code=200)
def delete_customer(customer_id: int):
    try:
        # First check if customer exists
        check_query = "SELECT customerId FROM Customers WHERE customerId = %s"
        customer = db.execute_single(check_query, (customer_id,))
        
        if not customer:
            raise HTTPException(
                status_code=404,
                detail=f"Customer with ID {customer_id} not found"
            )
        
        # Delete related reviews first
        delete_reviews_query = "DELETE FROM Reviews WHERE customerId = %s"
        db.execute_write(delete_reviews_query, (customer_id,))
        
        # Delete related orders
        delete_orders_query = "DELETE FROM Orders WHERE customerId = %s"
        db.execute_write(delete_orders_query, (customer_id,))
        
        # Delete the customer
        delete_query = "DELETE FROM Customers WHERE customerId = %s"
        rows_affected = db.execute_write(delete_query, (customer_id,))
        
        if rows_affected == 0:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete customer"
            )
            
        return {
            "message": "Customer and related orders/reviews deleted successfully",
            "customer_id": customer_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{customer_id}", status_code=200)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate
):
    try:
        # First check if customer exists
        check_query = "SELECT * FROM Customers WHERE customerId = %s"
        existing_customer = db.execute_single(check_query, (customer_id,))
        
        if not existing_customer:
            raise HTTPException(
                status_code=404,
                detail=f"Customer with ID {customer_id} not found"
            )
        
        # Build update query based on provided fields
        update_parts = []
        params = []
        
        if customer.firstName is not None:
            update_parts.append("firstName = %s")
            params.append(customer.firstName)
            
        if customer.lastName is not None:
            update_parts.append("lastName = %s")
            params.append(customer.lastName)
            
        if customer.addressState is not None:
            update_parts.append("addressState = %s")
            params.append(customer.addressState)
            
        # If no fields to update
        if not update_parts:
            return existing_customer
            
        # Construct and execute update query
        update_query = f"""
            UPDATE Customers 
            SET {', '.join(update_parts)}
            WHERE customerId = %s
        """
        params.append(customer_id)
        
        rows_affected = db.execute_write(update_query, params)
        
        if rows_affected == 0:
            raise HTTPException(
                status_code=500,
                detail="Failed to update customer"
            )
            
        # Fetch and return updated customer
        updated_customer = db.execute_single(check_query, (customer_id,))
        return {
            "message": "Customer updated successfully",
            "customer": updated_customer
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 