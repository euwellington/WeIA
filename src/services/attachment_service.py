from src.core.vector_store import VectorStore
from src.model.attachment import Attachment
from src.ingestion.text_loader import TextLoader

class AttachmentService:
    def __init__(self):
        self.proccess_file_and_return_embeddings = TextLoader()
        self.database = VectorStore()
        
    async def attachment_file(self, request: Attachment):
        
        try:
            chunks, embeddings, metadata = await self.proccess_file_and_return_embeddings.proccess_txt(request)
            
            self.database.create_collection_if_not_exists()
            
            self.database.save_data(chunks, embeddings, metadata)
            
            return {
                "message" : "Arquivo salvo com sucesso"
            }
            
        except Exception as e:
            raise f"erro: {e}"