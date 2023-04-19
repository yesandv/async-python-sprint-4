from http import HTTPStatus
from ipaddress import ip_address, ip_network

from fastapi import FastAPI
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response


class BlackListMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, black_list: set[str]):
        super().__init__(app)
        self.black_list = black_list

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        client_ip = request.headers.get("X-Forwarded-For")
        if client_ip:
            for ip in self.black_list:
                if ip_address(client_ip) in ip_network(ip):
                    return Response(status_code=HTTPStatus.FORBIDDEN)
        return await call_next(request)
