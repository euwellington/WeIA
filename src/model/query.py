from pydantic import BaseModel

class Query(BaseModel):
    description: str