from fastapi import APIRouter, HTTPException
from src.services.history_service import HistoryService
from fastapi.concurrency import run_in_threadpool

router = APIRouter()

class History:
    def __init__(self):
        self.history_service = HistoryService()
    
    async def get_history_by_session(self, session_id: str):
        try:
            history = await run_in_threadpool(self.history_service.get_history, session_id)
            return history
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def delete_history_by_session_id(self, session_id: str):
        try:
            history = await run_in_threadpool(self.history_service.delete_history, session_id)
            return history
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

controller = History()

router.get("/history_by_session/{session_id}")(controller.get_history_by_session)
router.delete("/history_by_session/{session_id}")(controller.delete_history_by_session_id)