import uuid
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from src.services.search_service import SearchService
from src.model.query import Query

router = APIRouter()

class SearchEndpoint:
    def __init__(self):
        self.search_service = SearchService()
        
    async def start_chat(self):
        session_id = str(uuid.uuid4())
        return {"session_id": session_id}
    
    async def search_context(self, request: Query):
        try:
            return await self.search_service.query(request)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        
controller = SearchEndpoint()

router.post('/search', summary="Faça busca pelo contexto anexado")(controller.search_context)
router.get("/start_chat", summary="Inicia nova conversa")(controller.start_chat)