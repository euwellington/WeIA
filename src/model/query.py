from pydantic import BaseModel

class Query(BaseModel):
    session_id: str
    description: str