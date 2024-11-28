from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from ...db.database import db

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

class ReviewCreate(BaseModel):
    customerId: int
    productId: int
    rating: int = Field(..., ge=1, le=10)  # Rating between 1 and 10

@router.post("/", status_code=201)
def create_review(review: ReviewCreate):
    try:
        # Verify if customer exists
        customer_query = "SELECT customerId FROM Customers WHERE customerId = %s"
        customer = db.execute_single(customer_query, (review.customerId,))
        if not customer:
            raise HTTPException(status_code=400, detail="Customer not found")
            
        # Verify if product exists
        product_query = "SELECT productId FROM Products WHERE productId = %s"
        product = db.execute_single(product_query, (review.productId,))
        if not product:
            raise HTTPException(status_code=400, detail="Product not found")
        
        # Get the maximum review ID
        max_id_query = "SELECT COALESCE(MAX(reviewId), 0) as max_id FROM Reviews"
        max_id_result = db.execute_single(max_id_query)
        new_review_id = max_id_result['max_id'] + 1
        
        # Insert the review
        insert_query = """
            INSERT INTO Reviews (
                reviewId,
                customerId,
                productId,
                rating
            ) VALUES (%s, %s, %s, %s)
        """
        
        params = (
            new_review_id,
            review.customerId,
            review.productId,
            review.rating
        )
        
        db.execute_write(insert_query, params)
        
        # Fetch the created review
        new_review = db.execute_single(
            "SELECT * FROM Reviews WHERE reviewId = %s",
            (new_review_id,)
        )
        
        return {"message": "Review created successfully", "review": new_review}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_reviews(
    customer_id: Optional[int] = None,
    product_id: Optional[int] = None,
    min_rating: Optional[int] = None,
    max_rating: Optional[int] = None
):
    try:
        query = "SELECT * FROM Reviews WHERE 1=1"
        params = []
        
        if customer_id:
            query += " AND customerId = %s"
            params.append(customer_id)
            
        if product_id:
            query += " AND productId = %s"
            params.append(product_id)
            
        if min_rating is not None:
            query += " AND rating >= %s"
            params.append(min_rating)
            
        if max_rating is not None:
            query += " AND rating <= %s"
            params.append(max_rating)
            
        query += " ORDER BY reviewId ASC"
        
        results = db.execute_many(query, params)
        return {"reviews": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{review_id}")
def get_review(review_id: int):
    try:
        query = "SELECT * FROM Reviews WHERE reviewId = %s"
        result = db.execute_single(query, (review_id,))
        
        if not result:
            raise HTTPException(status_code=404, detail="Review not found")
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{review_id}", status_code=200)
def delete_review(review_id: int):
    try:
        # Check if review exists
        check_query = "SELECT reviewId FROM Reviews WHERE reviewId = %s"
        review = db.execute_single(check_query, (review_id,))
        
        if not review:
            raise HTTPException(
                status_code=404,
                detail=f"Review with ID {review_id} not found"
            )
        
        # Delete the review
        delete_query = "DELETE FROM Reviews WHERE reviewId = %s"
        rows_affected = db.execute_write(delete_query, (review_id,))
        
        if rows_affected == 0:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete review"
            )
            
        return {
            "message": "Review deleted successfully",
            "review_id": review_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 