import redis
import json
from src.config.settings import settings

class HistoryService:
    def __init__(self):
        self.redis = redis.Redis.from_url(settings.REDIS_URL)

    def get_history(self, session_id: str, limit: int = 50):
        try:
            key = f"message_store:{session_id}"  # chave exata no Redis
            msgs = self.redis.lrange(key, -limit, -1)  # pega últimas 'limit' mensagens
            history_list = []

            for msg in msgs:
                try:
                    data = json.loads(msg)
                    # pega o conteúdo correto dentro de "data"
                    content = data.get("data", {}).get("content")
                    history_list.append({
                        "type": data.get("type"),
                        "content": content
                    })
                except Exception:
                    continue

            return history_list
        except Exception as e:
            print(f"Erro ao buscar histórico: {e}")
            return []
        
    def delete_history(self, session_id: str):
        try:
            key = f"message_store:{session_id}"
            deleted = self.redis.delete(key) 
            return {"deleted": bool(deleted)}
        except Exception as e:
            print(f"Erro ao deletar histórico: {e}")
            return {"deleted": False}