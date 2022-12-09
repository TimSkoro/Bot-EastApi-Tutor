from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.db.database import get_db, save
from models.db.models import DbNews
from models.pydentic.models import PydNews

news_router = APIRouter(prefix='/news', tags=['news'])


@news_router.get('/')
def all_news(db: Session = Depends(get_db)):
    result = db.query(DbNews).all()
    return {"result": result}


@news_router.post('/')
def create_news(new_news: PydNews, db: Session = Depends(get_db)):
    db_obj = DbNews(
        title=new_news.title,
        description=new_news.description,
    )
    save(db, db_obj)
    return {"result": db_obj}


@news_router.get('/{news_id}')
def get_news_by_id(news_id: int, db: Session = Depends(get_db)):
    result = db.query(DbNews).filter(DbNews.id == news_id).first()
    return {"result": result}


@news_router.delete('/{news_id}')
def get_news_by_id(news_id: int, db: Session = Depends(get_db)):
    result = db.query(DbNews).filter(DbNews.id == news_id).first()
    db.delete(result)
    db.commit()
    return {"result": 'killed'}

