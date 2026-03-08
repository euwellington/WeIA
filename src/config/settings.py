import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
    CHUNK_SIZE: int = int(os.environ.get('CHUNK_SIZE'))
    CHUNK_OVERLAP: int = int(os.environ.get('CHUNK_OVERLAP'))
    QDRANT_HOST: str = os.environ.get('QDRANT_HOST')
    QDRANT_API_KEY: str = os.environ.get('QDRANT_API_KEY')
    QDRANT_COLLECTION: str = os.environ.get('QDRANT_COLLECTION')
    GOOGLE_AI_API_KEY: str = os.environ.get('GOOGLE_AI_API_KEY')
    GOOGLE_AI_MODEL: str = os.environ.get('GOOGLE_AI_MODEL')
    EMBEDDINGS_MODEL: str = os.environ.get('EMBEDDINGS_MODEL')
    REDIS_URL: str = os.environ.get('REDIS_URL')
    
settings = Settings()