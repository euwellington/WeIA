import os
from src.core.vector_store import VectorStore
from src.model.attachment import Attachment
from src.ingestion.text_loader import TextLoader
from src.ingestion.pdf_loader import PdfLoader

class AttachmentService:
    def __init__(self):
        self.proccess_file_and_return_embeddings = TextLoader()
        self.proccess_pdf_and_return_embeddings = PdfLoader()
        self.database = VectorStore()
        
        
    async def attachment_file(self, request: Attachment):
        
        try:
            _, ext = os.path.splitext(request.attachment.filename)
            
            match ext:
                case ".txt":
                    chunks, embeddings, metadata = await self.proccess_file_and_return_embeddings.proccess_txt(request)
                case ".pdf":
                    chunks, embeddings, metadata = await self.proccess_pdf_and_return_embeddings.process_pdf(request)
                case ".docx":
                    return { "message" : "Funcionalidade em desenvolvimento" }
                case ".doc":
                    return { "message" : "Funcionalidade em desenvolvimento" }
                case ".csv":
                    return { "message" : "Funcionalidade em desenvolvimento" }
                case ".json":
                    return { "message" : "Funcionalidade em desenvolvimento" }
                case ".html":
                    return { "message" : "Funcionalidade em desenvolvimento" }
                case ".xml":
                    return { "message" : "Funcionalidade em desenvolvimento" }
                case _:
                    return { "message" : "Funcionalidade em desenvolvimento" }
            
            self.database.create_collection_if_not_exists()
            
            self.database.save_data(chunks, embeddings, metadata)
            
            return {
                "message" : "Arquivo salvo com sucesso",
                "erro" : False
            }
            
        except Exception as e:
            raise f"erro: {e}"
        