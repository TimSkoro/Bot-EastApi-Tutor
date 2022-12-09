from pydantic import BaseModel


class PydNews(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True
