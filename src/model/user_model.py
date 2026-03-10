from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: int
    company_id: int
    company_name: str
    name: str
    email: str
    password_hash: str
    created_at: datetime