import re
from src.core.embeddings import Embeddings
from src.core.vector_store import VectorStore
from src.core.llm import Llm

class SearchService:
    def __init__(self):
        self.embeddings = Embeddings()
        self.database = VectorStore()
        self.llm = Llm()
        
    def clean_text(self, text: str) -> str:
        text = text.replace("\r", " ").replace("\n", " ")
        text = re.sub(r"#", "", text)
        text = re.sub(r"-{2,}", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
        
    async def query(self, query: str):
        try:
            embeddings = self.embeddings.encode(query)
            
            context = ""
            
            points = self.database.load_context(embeddings).points
            
            for point in points:
                if point.payload['text']:
                    context += '\n' + self.clean_text(point.payload['text'])
            
            prompt_system = f"""
                - VOCÊ É UM ASSISTENTE VIRTUAL QYE SE CHAMA WeIA
                - SÓ RESPONDA ALGO SE TIVER NO CONTEXTO
                - CASO NÃO ENCONTRE NADA NO CONTEXT, RESPONDA ALGO HUMANO
                
                Context:
                {context}
            """
            
            response = await self.llm.generate("welligton_session_id", prompt_system, query)
            
            return response
            
        except Exception as e:
            raise f"Erro interno: {str(e)}"