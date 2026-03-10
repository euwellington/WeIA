import uuid
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
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
            generator = self.search_service.query(request)
            return StreamingResponse(
                self._stream_wrapper(generator),
                media_type="text/event-stream"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def _stream_wrapper(self, generator):
        async for chunk in generator:
            yield f"data: {json.dumps(chunk)}\n\n"

controller = SearchEndpoint()

router.post('/search')(controller.search_context)
router.get('/start_chat')(controller.start_chat)