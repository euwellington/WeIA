from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool

from src.services.auth_service import AuthService

router = APIRouter()


class AuthController:

    def __init__(self):
        self.auth_service = AuthService()

    async def login(self, email: str, password: str):
        try:

            user = await run_in_threadpool(
                self.auth_service.login,
                email,
                password
            )

            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Email ou senha inválidos"
                )

            return user

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


controller = AuthController()

router.post("/login")(controller.login)