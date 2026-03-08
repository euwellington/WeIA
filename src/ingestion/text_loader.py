from langchain_core.documents import Document
from src.model.attachment import Attachment
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config.settings import settings
from src.core.embeddings import Embeddings

class TextLoader:
    def __init__(self):
        self.embeddings = Embeddings()
    
    async def proccess_txt(self, file_txt: Attachment) -> tuple[list[str], list[list[float]]]:
        try:
            text_content = await file_txt.attachment.read()
            text_file = text_content.decode('utf-8')
            
            document = Document(
                page_content=text_file,
                metadata={"filename" : file_txt.attachment.filename}
            )
            
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP
            )
            
            docs = splitter.split_documents([document])
            
            chunks = [doc.page_content for doc in docs]
            
            embeddings = self.embeddings.encode(chunks)
            
            return chunks, embeddings, document.metadata
        except Exception as e:
            raise f"Erro interno: {e}"
        