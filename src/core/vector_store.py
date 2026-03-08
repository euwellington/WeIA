from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, Payload
from qdrant_client.http.exceptions import UnexpectedResponse, ResponseHandlingException
from src.config.settings import settings
from uuid import uuid4

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(
            url = settings.QDRANT_HOST,
            api_key = settings.QDRANT_API_KEY
        )
        
    
    def create_collection_if_not_exists(self):
        try:
            if not self.client.collection_exists(settings.QDRANT_COLLECTION):
                return self.client.create_collection(
                    settings.QDRANT_COLLECTION,
                    vectors_config=
                            VectorParams(
                                size = 384,
                                distance = Distance.COSINE
                            )
                    )        
            
        except UnexpectedResponse as e:
            raise Exception(f"Erro no Qdrant API: {e}")

        except ResponseHandlingException as e:
            raise Exception(f"Erro ao processar resposta do Qdrant: {e}")

        except Exception as e:
            raise Exception(f"Erro inesperado: {e}")
        
    def save_data(self, chunks, embeddings, metadata):
        try:
            points = []
            
            for chunk, embedding in zip(chunks, embeddings):
                points.append(
                    PointStruct(
                        id = str(uuid4()),
                        vector = embedding,
                        payload={
                            "text" : chunk,
                            "metadata" : metadata
                        }
                    )
                )
                
            return self.client.upsert(
                collection_name = settings.QDRANT_COLLECTION,
                points = points 
                )
            
        
        except UnexpectedResponse as e:
            raise Exception(f"Erro no Qdrant API: {e}")

        except ResponseHandlingException as e:
            raise Exception(f"Erro ao processar resposta do Qdrant: {e}")

        except Exception as e:
            raise Exception(f"Erro inesperado: {e}")
        
    
    def load_context(self, embeddings):
        try:
            return self.client.query_points(
                collection_name = settings.QDRANT_COLLECTION,
                query = embeddings,
                limit = 50
            )    
        
        except UnexpectedResponse as e:
            raise Exception(f"Erro no Qdrant API: {e}")

        except ResponseHandlingException as e:
            raise Exception(f"Erro ao processar resposta do Qdrant: {e}")

        except Exception as e:
            raise Exception(f"Erro inesperado: {e}")