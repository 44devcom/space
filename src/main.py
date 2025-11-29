from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import cars

app = FastAPI(
    title="Car Market API",
    description="API for managing car listings",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cars.router)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "car-market-api"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Car Market API",
        "version": "1.0.0",
        "docs": "/docs"
    }


