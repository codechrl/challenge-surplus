import inspect

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import Table, func

from db import db
from schema import image as schema
from schema.message import IdResponse, ImageResponse, Response
from util.file import upload
from util.validation import is_empty

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=ImageResponse)
async def get_image(
    id: int = None,
    name: str = None,
    file: str = None,
    enable: bool = None,
    page: int = 1,
    limit: int = 10,
    order_by: str = "id",
    asc: bool = True,
):
    try:
        database = db.get_database()
        table = Table("image", db.get_metadata(), autoload_with=db.get_engine())

        query = table.select()

        if id:
            query = query.where(table.c.id == id)
        if name:
            query = query.where(table.c.name == name)
        if file:
            query = query.where(table.c.file == file)
        if enable:
            query = query.where(table.c.enable == enable)

        total_count = await database.execute(
            query.with_only_columns(func.count(table.c.id).label("count"))
        )

        query = query.limit(limit).offset(limit * (page - 1))

        if asc:
            query = query.order_by(table.c[order_by].asc())
        else:
            query = query.order_by(table.c[order_by].desc())

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


@router.post("", status_code=status.HTTP_201_CREATED, response_model=IdResponse)
async def post_image(
    payload: schema.ImagePost = Depends(),
    file: UploadFile = File(...),
):
    try:
        database = db.get_database()
        table = Table("image", db.get_metadata(), autoload_with=db.get_engine())

        payload = dict(payload)
        payload["file"] = await upload("image", file)

        print(payload)

        query = table.insert().returning(table.c.id).values(payload)

        return_id = await database.execute(query)

        return Response(
            status="success",
            code=201,
            message=payload,
            data={"id": return_id},
            pagination=None,
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.put("", status_code=status.HTTP_200_OK, response_model=IdResponse)
async def put_image(
    id: int,
    payload: schema.ImagePost = Depends(),
    file: UploadFile = File(None),
):

    if await is_empty(table="image", conditions={"id": id}):
        raise HTTPException(status_code=409, detail=f"id {id} not exist")

    try:
        database = db.get_database()
        table = Table("image", db.get_metadata(), autoload_with=db.get_engine())

        payload = dict(payload)
        payload = {k: v for k, v in payload.items() if v is not None}
        if file:
            payload["file"] = await upload("image", file)

        query = (
            table.update()
            .returning(table.c.id)
            .where(table.c.id == id)
            .values(dict(payload))
        )

        return_id = await database.execute(query)

        return Response(
            status="success",
            code=201,
            message=payload,
            data={"id": return_id},
            pagination=None,
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete("", status_code=status.HTTP_200_OK, response_model=IdResponse)
async def delete_image(id: int):

    if await is_empty(table="image", conditions={"id": id}):
        raise HTTPException(status_code=409, detail=f"id {id} not exist")

    try:
        database = db.get_database()
        table = Table("image", db.get_metadata(), autoload_with=db.get_engine())

        query = table.delete().returning(table.c.id).where(table.c.id == id)

        return_id = await database.execute(query)

        return Response(
            status="success",
            code=201,
            message="delete data berhasil",
            data={"id": return_id},
            pagination=None,
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
