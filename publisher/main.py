from fastapi import FastAPI, Query
from google.cloud import pubsub_v1
import json
import os

app = FastAPI()
publisher = pubsub_v1.PublisherClient()

# Definindo variáveis de ambiente
PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_ID = os.getenv("TOPIC_ID")

topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

@app.post("/publish")
def publish_message(name: str, age: int, is_human: bool = Query(default=True, description="Set to False if not human")):
    # Cria a mensagem com o valor de is_human definido pelo usuário ou com o valor padrão
    message = {"name": name, "age": age, "isHuman": is_human}

    # Publica a mensagem no tópico
    future = publisher.publish(topic_path, json.dumps(message).encode("utf-8"))
    return {"message": "Message published", "id": future.result(), "content": message}

# Para rodar a API: uvicorn api_generate:app --reload --port 8001
