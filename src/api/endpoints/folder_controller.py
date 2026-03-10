from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool

from src.services.folder_service import FolderService

router = APIRouter()


class FolderController:

    def __init__(self):
        self.folder_service = FolderService()

    async def create_folder(self, company_id: int, user_id: int, name: str, description: str,  parent_id: int | None = None):
        try:
            return await run_in_threadpool(
                self.folder_service.create_folder,
                company_id,
                user_id,
                name,
                description,
                parent_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_folder(self, folder_id: int):
        try:
            return await run_in_threadpool(
                self.folder_service.get_folder,
                folder_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        
    async def list_by_company(self, company_id: int):
        try:
            return await run_in_threadpool(
                self.folder_service.list_by_company,
                company_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def list_user_folders(self, user_id: int):
        try:
            return await run_in_threadpool(
                self.folder_service.list_user_folders,
                user_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_folder(self, folder_id: int):
        try:
            return await run_in_threadpool(
                self.folder_service.delete_folder,
                folder_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


controller = FolderController()

router.post("/folders")(controller.create_folder)
router.get("/folders/{folder_id}")(controller.get_folder)
router.get("/folders/company/{company_id}")(controller.list_by_company)
router.get("/folders/user/{user_id}")(controller.list_user_folders)
router.delete("/folders/{folder_id}")(controller.delete_folder)