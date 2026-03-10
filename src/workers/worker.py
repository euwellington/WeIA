import redis
from rq import Queue
from rq.worker import SimpleWorker
from src.workers import upload_worker

print("Iniciando worker...")

print("Criando conexão com Redis...")
redis_conn = redis.Redis(
    host="localhost",
    port=6379
)

try:
    print("Testando conexão Redis...")
    response = redis_conn.ping()
    print("Redis conectado:", response)
except Exception as e:
    print("Erro ao conectar no Redis:", e)
    raise

print("Criando fila uploads...")
queue = Queue(
    "uploads",
    connection=redis_conn
)

print("Fila criada:", queue.name)

if __name__ == "__main__":
    print("Inicializando SimpleWorker...")
    worker = SimpleWorker([queue])

    print("Worker pronto")
    print("Escutando fila:", queue.name)

    worker.work()