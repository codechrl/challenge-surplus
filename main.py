from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from db import db
from routes import category, category_product, health, image, product, product_image

app = FastAPI(
    title="Surplus Challenge",
    version="0.1.0",
    description="API for Surplus Challenge",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(SessionMiddleware, secret_key="secret-key-challenge-surplus")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.router, prefix="/api/health", tags=["Health Test"])
app.include_router(category.router, prefix="/api/category", tags=["Category"])
app.include_router(product.router, prefix="/api/product", tags=["Product"])
app.include_router(
    category_product.router, prefix="/api/category-product", tags=["Category & Product"]
)
app.include_router(image.router, prefix="/api/image", tags=["Image"])
app.include_router(
    product_image.router, prefix="/api/product-image", tags=["Product & Image"]
)


@app.on_event("startup")
async def startup():
    await db.open_pool()


@app.on_event("shutdown")
async def shutdown():
    await db.close_pool()
