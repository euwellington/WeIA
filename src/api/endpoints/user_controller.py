from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool

from src.services.user_service import UserService

router = APIRouter()


class UserController:

    def __init__(self):
        self.user_service = UserService()

    async def create_user(self, company_id: int, name: str, email: str, password: str):
        try:
            return await run_in_threadpool(
                self.user_service.create_user,
                company_id,
                name,
                email,
                password
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_user(self, user_id: int):
        try:
            return await run_in_threadpool(
                self.user_service.get_user,
                user_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def list_users(self, company_id: int):
        try:
            return await run_in_threadpool(
                self.user_service.list_company_users,
                company_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_user(self, user_id: int):
        try:
            return await run_in_threadpool(
                self.user_service.delete_user,
                user_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


controller = UserController()

router.post("/users")(controller.create_user)
router.get("/users/{user_id}")(controller.get_user)
router.get("/users/company/{company_id}")(controller.list_users)
router.delete("/users/{user_id}")(controller.delete_user)