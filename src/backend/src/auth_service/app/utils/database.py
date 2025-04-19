from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from utils.settings import settings


def construct_db_url():
  return f"postgresql://{settings.options.database.user}:"\
                      f"{settings.options.database.password}@"\
                      f"{settings.options.database.host}:"\
                      f"{settings.options.database.port}/"\
                      f"{settings.options.database.db_name}"

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def create_tables():
  Base.metadata.create_all(bind=Engine)


Engine = create_engine(
  url = construct_db_url()
)

SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=Engine,
)

Base = declarative_base()
