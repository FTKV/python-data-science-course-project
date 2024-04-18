"""
Module of cars' schemas
"""

from datetime import datetime
import json
from typing import Annotated

from fastapi import UploadFile, File
from pydantic import BaseModel, Field, UUID4, ConfigDict

from src.utils.as_form import as_form


@as_form
class CarUnrecognizedPlateModel(BaseModel):
    plate: Annotated[UploadFile, File()]
    model: Annotated[str | None, Field(max_length=128)] = None
    color: Annotated[str | None, Field(max_length=32)] = None
    description: Annotated[str | None, Field(max_length=1024)] = None
    user_id: UUID4 | int | None = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


@as_form
class CarRecognizedPlateModel(BaseModel):
    plate: str = Field(min_length=3, max_length=32)
    model: Annotated[str | None, Field(max_length=128)] = None
    color: Annotated[str | None, Field(max_length=32)] = None
    description: Annotated[str | None, Field(max_length=1024)] = None
    user_id: UUID4 | int | None = None


@as_form
class CarUpdateModel(BaseModel):
    model: Annotated[str | None, Field(max_length=128)] = None
    color: Annotated[str | None, Field(max_length=32)] = None
    description: Annotated[str | None, Field(max_length=1024)] = None
    user_id: UUID4 | int | None = None


@as_form
class CarPatchModel(BaseModel):
    is_to_block: bool


class CarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 | int
    plate: str = Field(min_length=3, max_length=32)
    model: Annotated[str | None, Field(max_length=128)] = None
    color: Annotated[str | None, Field(max_length=32)] = None
    description: Annotated[str | None, Field(max_length=1024)] = None
    is_blocked: bool
    created_at: datetime
    updated_at: datetime
    user_id: UUID4 | int | None = None
