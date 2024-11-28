from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routers import product, health, category, customer, order, review

app = FastAPI(
    title="Online Shopping API",
    description="A simple FastAPI application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(customer.router)
app.include_router(order.router)
app.include_router(review.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)