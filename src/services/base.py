import abc
from typing import TypeVar, Generic

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logging_config import logger
from src.db import Base


class Repository(abc.ABC):
    @abc.abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryDB(
    Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(self, model: type(ModelType)):
        self._model = model

    async def get(self, *, session: AsyncSession, url_id: str) -> ModelType:
        statement = select(self._model).where(self._model.id == url_id)
        results = await session.execute(statement=statement)
        return results.scalar_one_or_none()

    async def create(
            self, *, session: AsyncSession, schema: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(schema)
        db_obj = self._model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self, *, session: AsyncSession, url_id: str, **kwargs
    ) -> ModelType:
        statement = (
            update(self._model)
            .where(self._model.id == url_id)
            .values(**kwargs)
        )
        await session.execute(statement=statement)
        await session.commit()
        return await self.get(session=session, url_id=url_id)

    async def ping(self, session: AsyncSession) -> dict:
        try:
            await session.execute(statement=select(self._model))
            res = {"message": "Database is up and running"}
        except OperationalError as ex:
            logger.exception("Error connecting to the database", ex)
            res = {"message": "Error connecting to the database"}
        return res
