import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from settings import settings

Base = declarative_base()


class Pool:
    async def open_pool(self):

        self.database = databases.Database(settings.PGSTRING)
        self.metadata = sqlalchemy.MetaData()
        self.engine = sqlalchemy.create_engine(
            settings.PGSTRING, pool_size=1, max_overflow=0
        )
        self.metadata.create_all(self.engine)
        await self.database.connect()
        print("INFO:", "    Connected to database")

    async def close_pool(self):
        await self.database.disconnect()

    def get_database(self):
        return self.database

    def get_metadata(self):
        return self.metadata

    def get_engine(self):
        return self.engine


db = Pool()
