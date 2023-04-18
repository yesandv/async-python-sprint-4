from .base import RepositoryDB
from ..models.url import UrlModel
from ..schemas.url import ShortUrl, UrlUpdate


class RepositoryUrl(RepositoryDB[UrlModel, ShortUrl, UrlUpdate]):
    pass


url_crud = RepositoryUrl(UrlModel)
