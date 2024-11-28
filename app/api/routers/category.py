from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ...db.database import db

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

# Category creation model
class CategoryCreate(BaseModel):
    categoryName: str = Field(..., min_length=1, max_length=50)

@router.post("/", status_code=201)
def create_category(category: CategoryCreate):
    try:
        # Get the maximum category ID
        max_id_query = "SELECT COALESCE(MAX(categoryId), 0) as max_id FROM Categories"
        max_id_result = db.execute_single(max_id_query)
        new_category_id = max_id_result['max_id'] + 1
        
        # Insert the category with the new ID
        insert_query = """
            INSERT INTO Categories (
                categoryId,
                categoryName
            ) VALUES (%s, %s)
        """
        
        params = (new_category_id, category.categoryName)
        
        try:
            db.execute_write(insert_query, params)
            
            # Fetch the created category
            new_category = db.execute_single(
                "SELECT * FROM Categories WHERE categoryId = %s",
                (new_category_id,)
            )
            
            return {"message": "Category created successfully", "category": new_category}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{category_id}", status_code=200)
def delete_category(category_id: int):
    try:
        # First check if category exists
        check_query = "SELECT categoryId FROM Categories WHERE categoryId = %s"
        category = db.execute_single(check_query, (category_id,))
        
        if not category:
            raise HTTPException(
                status_code=404,
                detail=f"Category with ID {category_id} not found"
            )
        
        # Check for related products
        products_query = "SELECT COUNT(*) as count FROM Products WHERE categoryId = %s"
        products_count = db.execute_single(products_query, (category_id,))
        
        if products_count and products_count['count'] > 0:
            # Delete all related products first
            delete_products_query = "DELETE FROM Products WHERE categoryId = %s"
            db.execute_write(delete_products_query, (category_id,))
        
        # Now delete the category
        delete_query = "DELETE FROM Categories WHERE categoryId = %s"
        rows_affected = db.execute_write(delete_query, (category_id,))
        
        if rows_affected == 0:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete category"
            )
            
        return {
            "message": "Category and all related products deleted successfully",
            "category_id": category_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_categories():
    try:
        query = "SELECT * FROM Categories ORDER BY categoryId"
        results = db.execute_many(query)
        return {"categories": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{category_id}")
def get_category(category_id: int):
    try:
        query = "SELECT * FROM Categories WHERE categoryId = %s"
        result = db.execute_single(query, (category_id,))
        
        if not result:
            raise HTTPException(status_code=404, detail="Category not found")
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 