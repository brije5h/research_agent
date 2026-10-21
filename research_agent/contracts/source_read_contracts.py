from pydantic import BaseModel, Field


class Source(BaseModel):
    title: str
    url: str
    content: str
    source_type: str = Field(default="other")

class SourceReadResponse(BaseModel):
    url: str
    title: str
    content: str
    source_type: str = Field(default="other")

class SourceReadError(BaseModel):
    url: str
    error: str = Field(default="failed to read source")