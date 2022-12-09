from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
db_instance_class = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = db_instance_class()
    try:
        yield db
    finally:
        db.close()


def save(db, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)


def makemigrations():
    Base.metadata.create_all(engine)
