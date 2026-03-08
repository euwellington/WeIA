from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import settings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import RedisChatMessageHistory

class Llm:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model = settings.GOOGLE_AI_MODEL,
            api_key = settings.GOOGLE_AI_API_KEY,
            temperature = 0.2
        )
        
    def get_memory(self, session_id: str):
        return RedisChatMessageHistory(
            session_id=session_id,
            url=settings.REDIS_URL,
            ttl=604800
        )
        
    async def generate(self, session_id: str, prompt_system: str, prompt_user: str):
        
        memory = self.get_memory(session_id)
        
        history = memory.messages
        
        messages = [
            SystemMessage(content=prompt_system),
            *history,
            HumanMessage(content=prompt_user)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        memory.add_user_message(prompt_user)
        memory.add_ai_message(response.content)
        
        return response.content