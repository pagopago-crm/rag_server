from app.core.service.rag_generation_service import RagGenerationService
from app.di_container import DIContainer
from app.api.model.response import RAGResponse
from app.api.model.request.rag_request import RAGRequest
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Form, UploadFile, File, Request
from typing import List


router = APIRouter()

@router.get("/generation/vector", response_model = RAGResponse)
def generate_rag(request: RAGRequest) -> JSONResponse:
    
    ragGenService = DIContainer.get(RagGenerationService)
    
    ragGenService.generation_rag(collection_name = request.collection_name)
    
    #응답 형식으로 변경
    return JSONResponse(content={
            "result" : "ok"
        })

## 멀티파트 형태로 벡터 추가데이터 넣기.
@router.post("/add/vector")
async def add_rag(request: Request) -> JSONResponse:
    
    ragGenService = DIContainer.get(RagGenerationService)
    
    formData = await request.form()
    
    
    temp = ragGenService.add_rag_data(
        collection_name = formData.get("collection_name")
        , formData = formData)
    
    return JSONResponse(content={
            "result" : "ok"
        })
    
@router.get("/health")
async def health_check():
    """서비스 상태 확인"""
    return {"status": "healthy", "service": "rag-generation"}
    
    


