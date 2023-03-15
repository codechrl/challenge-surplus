import inspect

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import Table, func

from db import db
from schema import category_product as schema
from schema.message import (
    CategoryProductDetailResponse,
    CategoryProductIdResponse,
    Response,
)
from util.validation import is_empty

router = APIRouter()


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=CategoryProductDetailResponse
)
async def get_category_product(
    category_id: int = None,
    product_id: int = None,
    page: int = 1,
    limit: int = 10,
):
    try:
        database = db.get_database()
        table = Table(
            "category_product", db.get_metadata(), autoload_with=db.get_engine()
        )
        table_product = Table(
            "product", db.get_metadata(), autoload_with=db.get_engine()
        )
        table_category = Table(
            "category", db.get_metadata(), autoload_with=db.get_engine()
        )

        query = table.select()
        query = query.with_only_columns(
            [
                table.c.product_id,
                table.c.category_id,
                table_product.c.name.label("product_name"),
                table_product.c.description.label("product_description"),
                table_product.c.enable.label("product_enable"),
                table_category.c.name.label("category_name"),
                table_category.c.enable.label("category_enable"),
            ]
        )

        if category_id:
            query = query.where(table.c.category_id == category_id)
        if product_id:
            query = query.where(table.c.product_id == product_id)

        total_count = await database.execute(
            query.with_only_columns(func.count(table.c.product_id).label("count"))
        )

        query = query.limit(limit).offset(limit * (page - 1))

        query = query.join(table_product, table.c.product_id == table_product.c.id)
        query = query.join(table_category, table.c.category_id == table_category.c.id)

        rows = await database.fetch_all(query)

        args, _, _, values = inspect.getargvalues(inspect.currentframe())
        args = {arg: values[arg] for arg in args if values[arg]}

        pagination = {
            "total_all": total_count,
            "total_page": len(rows),
            "page": page,
            "limit": limit,
        }

        return Response(
            status="success",
            code=200,
            message=args,
            data=rows,
            pagination=pagination,
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=CategoryProductIdResponse
)
async def post_category_product(payload: schema.CategoryProduct):

    payload = dict(payload)
    if await is_empty(table="category", conditions={"id": (payload["category_id"])}):
        raise HTTPException(
            status_code=409,
            detail=f"category_id { (payload['category_id'])} not exist",
        )
    if await is_empty(table="product", conditions={"id": (payload["product_id"])}):
        raise HTTPException(
            status_code=409,
            detail=f"product_id { (payload['product_id'])} not exist",
        )

    try:
        database = db.get_database()
        table = Table(
            "category_product", db.get_metadata(), autoload_with=db.get_engine()
        )

        payload = dict(payload)

        query = table.insert().values(payload)

        await database.execute(query)

        return Response(
            status="success",
            code=201,
            message="input data berhasil",
            data=payload,
            pagination=None,
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.put(
    "", status_code=status.HTTP_200_OK, response_model=CategoryProductIdResponse
)
async def put_category_product(
    product_id: int, category_id: int, payload: schema.CategoryProduct
):
    payload = dict(payload)
    if await is_empty(
        table="category_product",
        conditions={"product_id": product_id, "category_id": category_id},
    ):
        raise HTTPException(
            status_code=409,
            detail=f"category_product ({ product_id }, {category_id}) not exist",
        )
    if await is_empty(table="category", conditions={"id": (payload["category_id"])}):
        raise HTTPException(
            status_code=409,
            detail=f"category_id { (payload['category_id'])} not exist",
        )
    if await is_empty(table="product", conditions={"id": (payload["product_id"])}):
        raise HTTPException(
            status_code=409,
            detail=f"product_id { (payload['product_id'])} not exist",
        )

    try:
        database = db.get_database()
        table = Table(
            "category_product", db.get_metadata(), autoload_with=db.get_engine()
        )

        payload = dict(payload)
        payload = {k: v for k, v in payload.items() if v is not None}

        query = (
            table.update()
            .where(table.c.product_id == product_id)
            .where(table.c.category_id == category_id)
            .values(dict(payload))
        )

        await database.execute(query)

        return Response(
            status="success",
            code=200,
            message="edit data berhasil",
            data=payload,
            pagination=None,
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete(
    "", status_code=status.HTTP_200_OK, response_model=CategoryProductIdResponse
)
async def delete_category_product(product_id: int, category_id: int):

    if await is_empty(
        table="category_product",
        conditions={"product_id": product_id, "category_id": category_id},
    ):
        raise HTTPException(
            status_code=409,
            detail=f"category_product ({ product_id }, {category_id}) not exist",
        )
    try:
        database = db.get_database()
        table = Table(
            "category_product", db.get_metadata(), autoload_with=db.get_engine()
        )

        query = (
            table.delete()
            .where(table.c.product_id == product_id)
            .where(table.c.category_id == category_id)
        )

        await database.execute(query)

        return Response(
            status="success",
            code=200,
            message="hapus data berhasil",
            data={"product_id": product_id, "category_id": category_id},
            pagination=None,
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
