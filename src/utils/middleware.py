from http import HTTPStatus
from typing import Callable

from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response


class BlackListMiddleware(BaseModel):
    black_list: set[str]

    async def __call__(
            self, request: Request, call_next: Callable
    ) -> Response:
        if request.client.host in self.black_list:
            return Response(status_code=HTTPStatus.FORBIDDEN)
        return await call_next(request)
