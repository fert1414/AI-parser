from pydantic import BaseModel, HttpUrl

class AnalyzeSourceRequest(BaseModel):
    source_links: list[HttpUrl]

class FoundSource(BaseModel):
    source_link: str
    rss_link: str | None

class AnalyzeSourceResponse(BaseModel):
    result: list[FoundSource]