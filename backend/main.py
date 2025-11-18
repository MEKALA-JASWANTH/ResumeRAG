from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import shutil
from pathlib import Path
import logging

from rag_engine.rag_pipeline import RAGPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ResumeRAG API",
    description="AI-Powered Career Intelligence Platform - RAG system for competitive exam prep & job search",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

rag_pipeline = None

def get_rag_pipeline():
    global rag_pipeline
    if rag_pipeline is None:
        logger.info("Initializing RAG Pipeline...")
        rag_pipeline = RAGPipeline()
    return rag_pipeline

class QueryRequest(BaseModel):
    query: str
    k: int = 5
    filter_metadata: Optional[Dict] = None

class QueryResponse(BaseModel):
    query: str
    results: List[Dict]
    num_results: int

class IndexResponse(BaseModel):
    status: str
    message: str
    files_processed: int
    chunks_created: int

@app.on_event("startup")
async def startup_event():
    logger.info("Starting ResumeRAG API...")
    get_rag_pipeline()
    logger.info("ResumeRAG API started successfully!")

@app.get("/")
async def root():
    return {
        "message": "Welcome to ResumeRAG API",
        "description": "AI-Powered Career Intelligence Platform",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "upload": "/upload - Upload documents for indexing",
            "query": "/query - Search your documents",
            "stats": "/stats - Get system statistics",
            "health": "/health - Health check"
        }
    }

@app.post("/upload", response_model=IndexResponse)
async def upload_documents(files: List[UploadFile] = File(...)):
    try:
        saved_paths = []
        
        for file in files:
            if not file.filename.endswith(('.pdf', '.docx', '.txt')):
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {file.filename}. Only PDF, DOCX, and TXT are supported."
                )
            
            file_path = UPLOAD_DIR / file.filename
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            saved_paths.append(str(file_path))
            logger.info(f"Saved file: {file.filename}")
        
        pipeline = get_rag_pipeline()
        result = pipeline.index_documents(saved_paths)
        
        return IndexResponse(
            status="success",
            message=f"Successfully indexed {len(files)} file(s)",
            files_processed=result.get('files_processed', len(files)),
            chunks_created=result.get('chunks', 0)
        )
        
    except Exception as e:
        logger.error(f"Error uploading documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        pipeline = get_rag_pipeline()
        results = pipeline.search(
            query=request.query,
            k=request.k,
            filter_dict=request.filter_metadata
        )
        
        return QueryResponse(
            query=results['query'],
            results=results['results'],
            num_results=results['num_results']
        )
        
    except Exception as e:
        logger.error(f"Error querying documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    try:
        pipeline = get_rag_pipeline()
        stats = pipeline.get_stats()
        
        return {
            "status": "success",
            "data": stats
        }
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    try:
        pipeline = get_rag_pipeline()
        return {
            "status": "healthy",
            "message": "ResumeRAG API is running",
            "pipeline_initialized": pipeline is not None
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": str(e)
        }

@app.delete("/documents")
async def clear_documents():
    try:
        for file in UPLOAD_DIR.glob("*"):
            if file.is_file():
                file.unlink()
        
        return {
            "status": "success",
            "message": "All documents cleared"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
