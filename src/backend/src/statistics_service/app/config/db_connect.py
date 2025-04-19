from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


class DB():
    Base = declarative_base()

    def __init__(self):
        SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@statistics_database/statistics_db"
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL)
        self.SesionLocal = sessionmaker(autoflush=False, autocommit=False, bind=self.engine)
        self.Base.metadata.create_all(bind=self.engine)

    def get_db(self):
        db = self.SesionLocal()
        try:
            yield db
        finally:
            db.close()
