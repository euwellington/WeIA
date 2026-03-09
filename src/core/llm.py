import uuid
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import settings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import RedisChatMessageHistory
from src.model.query import Query

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

    async def generate(self, prompt_system: str, prompt_user: Query):
        memory = self.get_memory(prompt_user.session_id)
        history = memory.messages

        past_messages = []
        for msg in history:
            if hasattr(msg, "type") and hasattr(msg, "content"):
                if msg.type == "human":
                    past_messages.append(HumanMessage(content=msg.content))
                elif msg.type == "ai":
                    past_messages.append(SystemMessage(content=msg.content))

        messages = [
            SystemMessage(content=prompt_system),
            *past_messages,
            HumanMessage(content=prompt_user.description)
        ]

        response = await self.llm.ainvoke(messages)
        memory.add_user_message(prompt_user.description)
        memory.add_ai_message(response.content)

        return {
            "session_id": prompt_user.session_id,
            "response": response.content
        }