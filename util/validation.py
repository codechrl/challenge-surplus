from sqlalchemy import Table

from db import db


async def is_empty(table, conditions):
    database = db.get_database()
    table = Table(table, db.get_metadata(), autoload_with=db.get_engine())

    query = table.select()

    for key, value in conditions.items():
        query = query.where(table.c[key] == value)

    return True if (await database.fetch_one(query)) is None else False
