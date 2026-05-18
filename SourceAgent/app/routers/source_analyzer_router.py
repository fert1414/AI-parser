from fastapi import APIRouter, HTTPException

from app.core.exceptions import SourceAgentError
from app.schemas.source_analyzer_schemas import AnalyzeSourceRequest, AnalyzeSourceResponse
from app.services.source_agent import SourceAgent

router = APIRouter(prefix="/sources", tags=["sources"])

source_agent = SourceAgent()

@router.post("/analyze", response_model = AnalyzeSourceResponse)
def analyze_source(request: AnalyzeSourceRequest):
    try:
        source_extraction_links = source_agent.analyze_sources(request.source_links)

        return AnalyzeSourceResponse(result = source_extraction_links)
    
    except SourceAgentError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected source analyzer error: {exc}"
        )