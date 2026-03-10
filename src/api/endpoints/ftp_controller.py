from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool

from src.services.ftp_service import FtpService

router = APIRouter()


class FtpController:

    def __init__(self):
        self.ftp_service = FtpService()


    async def delete_file(self, path: str):
        try:
            return await run_in_threadpool(
                self.ftp_service.delete_file,
                path
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


controller = FtpController()

router.delete("/ftp")(controller.delete_file)