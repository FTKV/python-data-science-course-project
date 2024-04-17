"""
Module of rates' schemas
"""

from typing import Annotated
from pydantic import BaseModel, Field, UUID4, ConfigDict
from typing import Optional

from src.utils.as_form import as_form


@as_form
class RateModel(BaseModel):
    title: Annotated[str, Field(min_length=2, max_length=32)]
    description: Annotated[str | None, Field(max_length=1024)] = None
    is_daily: bool = False


@as_form
class RateUpdate(BaseModel):
    title: Annotated[str | None, Field(min_length=2, max_length=32)] = None
    description: Annotated[str | None, Field(max_length=1024)] = None
    is_daily: bool | None = None


class RateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 | int
    title: Annotated[str, Field(min_length=2, max_length=32)]
    description: Annotated[str | None, Field(max_length=1024)] = None
    is_daily: bool = False
