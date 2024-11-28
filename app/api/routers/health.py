from fastapi import APIRouter, HTTPException
from ...db.database import db

router = APIRouter(
    tags=["health"]
)

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/db-test")
def test_db():
    try:
        result = db.execute_single("SELECT 1 as test")
        if result is None:
            return {"message": "No results found"}
        return {"message": "Database connection successful!", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 