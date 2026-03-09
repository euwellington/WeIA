from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import settings

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    AIMessage
)

from langchain_community.chat_message_histories import RedisChatMessageHistory


class Llm:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model=settings.GOOGLE_AI_MODEL,
            api_key=settings.GOOGLE_AI_API_KEY,
            temperature=0.2
        )


    def get_memory(self, session_id: str):

        return RedisChatMessageHistory(
            session_id=session_id,
            url=settings.REDIS_URL,
            ttl=604800
        )


    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        session_id: str
    ):

        memory = self.get_memory(session_id)

        history = memory.messages[-10:]

        past_messages = []

        for msg in history:

            if hasattr(msg, "type") and hasattr(msg, "content"):

                if msg.type == "human":
                    past_messages.append(HumanMessage(content=msg.content))

                elif msg.type == "ai":
                    past_messages.append(AIMessage(content=msg.content))


        messages = [
            SystemMessage(content=system_prompt),
            *past_messages,
            HumanMessage(content=user_prompt)
        ]


        full_response = ""


        async for chunk in self.llm.astream(messages):

            content = chunk.content or ""

            full_response += content

            yield content


        memory.add_user_message(user_prompt)
        memory.add_ai_message(full_response)


    async def simple_completion(self, prompt: str):

        messages = [
            HumanMessage(content=prompt)
        ]

        response = await self.llm.ainvoke(messages)

        return response.content


    async def rewrite_query(self, question: str):

        prompt = f"""
Reescreva a pergunta abaixo para melhorar uma busca semântica em documentos.

Regras:
- mantenha o significado original
- torne a consulta mais clara
- adicione palavras-chave relevantes
- responda apenas com a nova consulta

Pergunta:
{question}
"""

        response = await self.simple_completion(prompt)

        return response.strip()