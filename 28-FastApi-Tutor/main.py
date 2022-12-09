from fastapi import FastAPI
from apps.news.views import news_router
from models.db.database import makemigrations

app = FastAPI()
app.include_router(news_router)


@app.get('/migration')
def migrate():
    makemigrations()
    return {"status": "done"}