from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from src.services.file_service import FileService

router = APIRouter()

class FileController:

    def __init__(self):
        self.file_service = FileService()

    async def upload_file(self, company_id: int, user_id: int, folder_id: int, file: UploadFile):
        try:
            return await self.file_service.upload_file(
                company_id,
                user_id,
                folder_id,
                file
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def list_files(self, folder_id: int):
        try:
            return await run_in_threadpool(
                self.file_service.list_files,
                folder_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_file(self, file_id: int):
        try:
            return await run_in_threadpool(
                self.file_service.delete_file,
                file_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

controller = FileController()

router.post("/files/upload")(controller.upload_file)
router.get("/files/folder/{folder_id}")(controller.list_files)
router.delete("/files/{file_id}")(controller.delete_file)