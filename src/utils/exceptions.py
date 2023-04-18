from fastapi import HTTPException
from starlette import status

from src.models import UrlModel


class GoneException(Exception):

    def __init__(self, url: UrlModel):
        if url.is_taken_down:
            raise HTTPException(
                status_code=status.HTTP_410_GONE, detail="Gone"
            )
