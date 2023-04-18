from pydantic import BaseModel, HttpUrl


class FullUrl(BaseModel):
    full_url: HttpUrl

    class Config:
        orm_mode = True


class ShortUrl(BaseModel):
    id: str

    class Config:
        orm_mode = True


class UrlUpdate(ShortUrl):
    clicks: int
    is_taken_down: bool


class UrlInDB(BaseModel):
    id: str
    full_url: HttpUrl
    clicks: int
    is_taken_down: bool

    class Config:
        orm_mode = True
