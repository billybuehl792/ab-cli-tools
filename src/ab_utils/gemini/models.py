from enum import Enum
from pathlib import Path
from typing import Generic, TypeVar
from pydantic import BaseModel, Field

from .constants import DEFAULT_GEMINI_MODEL

T = TypeVar("T", bound=BaseModel)


class ResponseMimeType(str, Enum):
    TEXT = "text/plain"
    JSON = "application/json"


class GeminiOptions(BaseModel, Generic[T]):
    model: str = DEFAULT_GEMINI_MODEL
    files: list[Path] = Field(default_factory=list)
    response_mime_type: ResponseMimeType = ResponseMimeType.TEXT
    response_schema: type[T] | None = None
