from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped

from src.db import Base
from src.utils.str_gen import get_char_id


class UrlModel(Base):
    __tablename__ = "short_urls"

    id: Mapped[str] = Column(
        String, primary_key=True, default=get_char_id, unique=True
    )
    full_url: Mapped[str] = Column(String, nullable=False, unique=False)
    clicks: Mapped[int] = Column(Integer, default=0)
    is_taken_down: Mapped[bool] = Column(
        Boolean, nullable=False, default=False
    )
