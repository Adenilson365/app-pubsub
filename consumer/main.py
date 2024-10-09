from fastapi import FastAPI, Request
from google.cloud import pubsub_v1
import json
import base64
import os

app = FastAPI()

# Definindo variáveis de ambiente
PROJECT_ID = os.getenv("PROJECT_ID")
DLQ_TOPIC_ID = os.getenv("DLQ_TOPIC_ID")

dlq_topic_path = f"projects/{PROJECT_ID}/topics/{DLQ_TOPIC_ID}"
publisher = pubsub_v1.PublisherClient()

@app.post("/receive")
async def receive_message(request: Request):
    envelope = await request.json()
    message_data = envelope["message"]["data"]
    message = json.loads(base64.b64decode(message_data).decode("utf-8"))

    # Verifica se o campo isHuman é False
    if not message.get("isHuman", True):
        # Se isHuman for False, publica na fila DLQ
        publisher.publish(dlq_topic_path, json.dumps(message).encode("utf-8"))
        return {"status": "Message sent to DLQ", "message": message}

    # Caso contrário, processa a mensagem
    return {"status": "Message accepted", "message": message}

# Para rodar a API: uvicorn api_filter:app --reload --port 8002
