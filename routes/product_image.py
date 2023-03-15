import inspect

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import Table, func

from db import db
from schema import product_image as schema
from schema.message import ProductImageDetailResponse, ProductImageIdResponse, Response
from util.validation import is_empty

router = APIRouter()


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=ProductImageDetailResponse
)
async def get_product_image(
    product_id: int = None,
    image_id: int = None,
    page: int = 1,
    limit: int = 10,
    order_by: str = "product_id",
    asc: bool = True,
):
    try:
        database = db.get_database()
        table = Table("product_image", db.get_metadata(), autoload_with=db.get_engine())
        table_product = Table(
            "product", db.get_metadata(), autoload_with=db.get_engine()
        )
        table_image = Table("image", db.get_metadata(), autoload_with=db.get_engine())

        query = table.select()
        query = query.with_only_columns(
            [
                table.c.product_id,
                table.c.image_id,
                table_product.c.name.label("product_name"),
                table_product.c.description.label("product_description"),
                table_product.c.enable.label("product_enable"),
                table_image.c.name.label("image_name"),
                table_image.c.file.label("image_file"),
                table_image.c.enable.label("image_enable"),
            ]
        )

        if image_id:
            query = query.where(table.c.image_id == image_id)
        if product_id:
            query = query.where(table.c.product_id == product_id)

        total_count = await database.execute(
            query.with_only_columns(func.count(table.c.product_id).label("count"))
        )

        query = query.limit(limit).offset(limit * (page - 1))

        if asc:
            query = query.order_by(table.c[order_by].asc())
        else:
            query = query.order_by(table.c[order_by].desc())

        query = query.join(table_product, table.c.product_id == table_product.c.id)
        query = query.join(table_image, table.c.image_id == table_image.c.id)

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
    "", status_code=status.HTTP_201_CREATED, response_model=ProductImageIdResponse
)
async def post_product_image(payload: schema.ProductImage):

    payload = dict(payload)
    if await is_empty(table="image", conditions={"id": (payload["image_id"])}):
        raise HTTPException(
            status_code=409,
            detail=f"image_id { (payload['image_id'])} not exist",
        )
    if await is_empty(table="product", conditions={"id": (payload["product_id"])}):
        raise HTTPException(
            status_code=409,
            detail=f"product_id { (payload['product_id'])} not exist",
        )

    try:
        database = db.get_database()
        table = Table("product_image", db.get_metadata(), autoload_with=db.get_engine())

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


@router.put("", status_code=status.HTTP_200_OK, response_model=ProductImageIdResponse)
async def put_product_image(
    product_id: int, image_id: int, payload: schema.ProductImage
):
    payload = dict(payload)
    if await is_empty(
        table="product_image",
        conditions={"product_id": product_id, "image_id": image_id},
    ):
        raise HTTPException(
            status_code=409,
            detail=f"product_image ({ product_id }, {image_id}) not exist",
        )
    if await is_empty(table="image", conditions={"id": (payload["image_id"])}):
        raise HTTPException(
            status_code=409,
            detail=f"image_id { (payload['image_id'])} not exist",
        )
    if await is_empty(table="product", conditions={"id": (payload["product_id"])}):
        raise HTTPException(
            status_code=409,
            detail=f"product_id { (payload['product_id'])} not exist",
        )

    try:
        database = db.get_database()
        table = Table("product_image", db.get_metadata(), autoload_with=db.get_engine())

        payload = dict(payload)
        payload = {k: v for k, v in payload.items() if v is not None}

        query = (
            table.update()
            .where(table.c.product_id == product_id)
            .where(table.c.image_id == image_id)
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
    "", status_code=status.HTTP_200_OK, response_model=ProductImageIdResponse
)
async def delete_product_image(product_id: int, image_id: int):

    if await is_empty(
        table="product_image",
        conditions={"product_id": product_id, "image_id": image_id},
    ):
        raise HTTPException(
            status_code=409,
            detail=f"product_image ({ product_id }, {image_id}) not exist",
        )
    try:
        database = db.get_database()
        table = Table("product_image", db.get_metadata(), autoload_with=db.get_engine())

        query = (
            table.delete()
            .where(table.c.product_id == product_id)
            .where(table.c.image_id == image_id)
        )

        await database.execute(query)

        return Response(
            status="success",
            code=200,
            message="hapus data berhasil",
            data={"product_id": product_id, "image_id": image_id},
            pagination=None,
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
