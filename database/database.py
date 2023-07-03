from sqlalchemy import create_engine

from database.models import Base

engine = create_engine("sqlite+pysqlite:///bot.db", echo=True)
Base.metadata.create_all(engine)
