from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool

from src.services.company_service import CompanyService

router = APIRouter()


class CompanyController:

    def __init__(self):
        self.company_service = CompanyService()

    async def create_company(self, name: str):
        try:
            return await run_in_threadpool(
                self.company_service.create_company,
                name
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def list_companies(self):
        try:
            return await run_in_threadpool(
                self.company_service.list_companies
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_company(self, company_id: int):
        try:
            return await run_in_threadpool(
                self.company_service.get_company,
                company_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_company(self, company_id: int):
        try:
            return await run_in_threadpool(
                self.company_service.delete_company,
                company_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


controller = CompanyController()

router.post("/companies")(controller.create_company)
router.get("/companies")(controller.list_companies)
router.get("/companies/{company_id}")(controller.get_company)
router.delete("/companies/{company_id}")(controller.delete_company)