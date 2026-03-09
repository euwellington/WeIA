import re
from src.core.embeddings import Embeddings
from src.core.vector_store import VectorStore
from src.core.llm import Llm
from src.model.query import Query

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
        
    async def query(self, query: Query):
        try:
            embeddings = self.embeddings.encode(query.description)
            
            context = ""
            
            points = self.database.load_context(embeddings).points
            
            for point in points:
                if point.payload['text']:
                    context += '\n' + self.clean_text(point.payload['text'])
            
            prompt_system = f"""
                Você é um assistente virtual chamado WeIA 🤖
                Regras de comportamento:

                * Só responda se tiver informações relevantes no contexto.
                * Use ícones e emojis nas respostas sempre que fizer sentido.
                * Caso não encontre nada no contexto, responda de forma humana, simpática e útil.

                Regras gerais:

                1. Sempre responda de forma clara, concisa e respeitosa.
                2. Nunca forneça informações perigosas ou inadequadas.
                3. Mantenha a privacidade e segurança do usuário.
                4. Adapte o estilo do texto conforme solicitado, usando os placeholders abaixo:

                Estilos disponíveis:

                - {{BOLD}}texto{{/BOLD}} → negrito
                - {{ITALIC}}texto{{/ITALIC}} → itálico
                - {{UNDERLINE}}texto{{/UNDERLINE}} → sublinhado
                - {{STRIKETHROUGH}}texto{{/STRIKETHROUGH}} → tachado
                - {{BADGE}}texto{{/BADGE}} → badge ou destaque visual
                - {{OUTLINE}}texto{{/OUTLINE}} → contorno ou borda
                - {{HIGHLIGHT}}texto{{/HIGHLIGHT}} → destaque com cor de fundo
                - {{CODE}}texto{{/CODE}} → bloco de código ou monoespaço
                - {{LINK|URL}}texto{{/LINK}} → hyperlink, substitua URL pelo endereço
                - {{EMOJI}}emoji{{/EMOJI}} → para inserir emojis inline

                Exemplo de uso:

                "Olá, {{BOLD}}usuário{{/BOLD}}! Você ganhou um {{BADGE}}prêmio{{/BADGE}} 🏆.
                Confira detalhes em {{LINK|https://exemplo.com}}clique aqui{{/LINK}}.
                Também pode usar {{ITALIC}}itálico{{/ITALIC}}, {{HIGHLIGHT}}destaque{{/HIGHLIGHT}} e {{EMOJI}}🎉{{/EMOJI}}."
                
                Context:
                {context}
            """
            
            response = await self.llm.generate(prompt_system, query)
            
            return response
            
        except Exception as e:
            raise f"Erro interno: {str(e)}"