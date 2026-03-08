from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from src.services.search_service import SearchService
from src.model.query import Query

router = APIRouter()

class SearchEndpoint:
    def __init__(self):
        self.search_service = SearchService()
    
    async def search_context(self, request: Query):
        try:
            return await self.search_service.query(request.description)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        
controller = SearchEndpoint()

router.post('/search', summary="Faça busca pelo contexto anexado")(controller.search_context)