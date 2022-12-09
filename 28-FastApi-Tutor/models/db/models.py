from sqlalchemy import Column, Integer, String

from models.db.database import Base


class DbNews(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
