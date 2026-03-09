from src.core.embeddings import Embeddings
from src.model.attachment import Attachment
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pypdf import PdfReader

from io import BytesIO


class PdfLoader:
    def __init__(self):
        self.embeddings = Embeddings()

    async def process_pdf(self, document: Attachment):
        try:

            file_bytes = await document.attachment.read()

            pdf = PdfReader(BytesIO(file_bytes))

            documents = []

            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": document.attachment.filename,
                                "page": i + 1
                            }
                        )
                    )

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=120
            )

            docs = splitter.split_documents(documents)

            chunks = [doc.page_content for doc in docs]
            metadata = [doc.metadata for doc in docs]

            embeddings = self.embeddings.encode(chunks)

            return chunks, embeddings, metadata

        except Exception as e:
            raise Exception(f"Erro interno: {str(e)}")