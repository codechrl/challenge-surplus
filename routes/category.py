from fastapi import APIRouter, status
from sqlalchemy import Table, func

from db import db
from schema import category as schema
from schema.message import Response, ResponseHTTPException

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def get_category(
    id: int = None,
    name: str = None,
    enable: bool = None,
    page: int = 1,
    limit: int = 10,
):
    try:
        database = db.get_database()
        table = Table("category", db.get_metadata(), autoload_with=db.get_engine())

        query = table.select()

        total_count = await database.execute(
            query.with_only_columns(func.count(table.c.id).label("count"))
        )

        if id:
            query = query.where(table.c.id == id)
        if name:
            query = query.where(table.c.name == name)
        if enable:
            query = query.where(table.c.enable == enable)

        query = query.limit(limit).offset(limit * (page - 1))
        rows = await database.fetch_all(query)

        pagination = {
            "total": total_count,
            "page": page,
            "limit": limit,
        }

        return Response(
            status="success",
            code=200,
            data=rows,
            pagination=pagination,
        )

    except Exception as exc:
        raise ResponseHTTPException(message=exc)


@router.post("", status_code=status.HTTP_201_CREATED)
async def post_category(payload: schema.CategoryPost):
    try:
        database = db.get_database()
        table = Table("category", db.get_metadata(), autoload_with=db.get_engine())

        query = table.insert().returning(table.c.id).values(dict(payload))

        return_id = await database.execute(query)
        return {"message": "input data berhasil", "id": return_id}

    except Exception as exc:
        raise ResponseHTTPException(message=exc)


@router.put("", status_code=status.HTTP_200_OK)
async def put_category(id: int, payload: schema.CategoryPut):
    try:
        database = db.get_database()
        table = Table("category", db.get_metadata(), autoload_with=db.get_engine())

        payload = dict(payload)
        payload = {k: v for k, v in payload.items() if v is not None}

        query = (
            table.update()
            .returning(table.c.id)
            .where(table.c.id == id)
            .values(dict(payload))
        )

        return_id = await database.execute(query)
        return {"message": "edit data berhasil", "id": return_id}

    except Exception as exc:
        raise ResponseHTTPException(message=exc)


@router.delete("", status_code=status.HTTP_200_OK)
async def delete_category(id: int):
    try:
        database = db.get_database()
        table = Table("category", db.get_metadata(), autoload_with=db.get_engine())

        query = table.delete().returning(table.c.id).where(table.c.id == id)

        return_id = await database.execute(query)
        return {"message": "hapus data berhasil", "id": return_id}

    except Exception as exc:
        raise ResponseHTTPException(message=exc)
