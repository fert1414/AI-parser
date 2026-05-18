import uvicorn
from fastapi import FastAPI

from app.routers.source_analyzer_router import router as source_analyzer_router

app = FastAPI(
    title="Resource Analyzer Service",
    version = "0.1.0"
)

app.include_router(source_analyzer_router, prefix="/api/v1")

app.get("/health")
def health_check():
    return {"status": "ok"}

def main():
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )

if __name__ == "__main__":
    main()