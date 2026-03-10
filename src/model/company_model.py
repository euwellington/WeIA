from pydantic import BaseModel
from datetime import datetime


class Company(BaseModel):
    id: int
    name: str
    created_at: datetime