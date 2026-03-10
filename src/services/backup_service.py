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

            yield {"type": "status", "message": "otimizando_consulta"}

            optimized_query = await self.llm.rewrite_query(query.description)

            yield {"type": "status", "message": "buscando_contexto"}

            embeddings = self.embeddings.encode(optimized_query)

            result = self.database.load_context(embeddings)

            points = result.points

            context = ""
            seen_texts = set()

            MAX_CONTEXT = 12000

            for point in points:

                payload = point.payload or {}

                if payload.get("text"):

                    text = self.clean_text(payload["text"])

                    key = text[:120]

                    if key in seen_texts:
                        continue

                    seen_texts.add(key)

                    context += "\n" + text

                    yield {
                        "type": "document",
                        "content": text[:200]
                    }

                    if len(context) > MAX_CONTEXT:
                        break

            yield {"type": "status", "message": "gerando_resposta"}

            prompt_system = """
            Você é um assistente de IA chamado WeIA.

            Responda de forma clara, objetiva e útil.

            Quando houver contexto fornecido, utilize-o como principal fonte da resposta.

            Se o contexto não tiver informação suficiente, utilize conhecimento geral para complementar.

            Organize respostas complexas com listas ou seções quando necessário.
            
            CONTEXTO:
            {context}
            """

            async for chunk in self.llm.generate(
                system_prompt=prompt_system,
                user_prompt=query,
                session_id=query.session_id
            ):
                yield {
                    "type": "token",
                    "content": chunk
                }

            yield {"type": "done"}

        except Exception as e:

            yield {
                "type": "error",
                "message": str(e)
            }