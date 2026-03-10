from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Folder(BaseModel):
    id: int
    company_id: int
    user_id: int
    name: str
    description: str
    parent_id: Optional[int]
    created_at: datetime