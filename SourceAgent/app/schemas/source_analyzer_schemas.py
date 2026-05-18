from pydantic import BaseModel, HttpUrl

# ------------------------------------Requests------------------------------------

class AnalyzeSourceRequest(BaseModel):
    source_links: list[HttpUrl]

# ------------------------------------Responses------------------------------------

class Fields(BaseModel):
    title: bool = False
    link: bool = False
    summary: bool = False
    published: bool = False

class FoundSource(BaseModel):
    source_link: str
    source_type: str | None = None
    feed_link: str | None = None
    feed_format: str | None = None
    fields: Fields

class AnalyzeSourceResponse(BaseModel):
    result: list[FoundSource]