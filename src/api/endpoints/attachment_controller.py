from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from src.model.attachment import Attachment
from src.services.attachment_service import AttachmentService

router = APIRouter()

class AttachmentEndpoint:
    def __init__(self):
        self.attachment_service = AttachmentService()
    
    async def attachment(self, request: Attachment = Depends()):
        try:
            
            action = await self.attachment_service.attachment_file(request)
            
            return action
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))  
        
controller = AttachmentEndpoint()

router.post("/attachment", summary="Anexar um novo arquivo")(controller.attachment)