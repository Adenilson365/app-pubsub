from fastapi import FastAPI
from google.cloud import pubsub_v1
import json
import os

app = FastAPI()

PROJECT_ID = os.getenv("PROJECT_ID")
DLQ_SUBSCRIPTION_ID = os.getenv("DLQ_SUBSCRIPTION_ID")

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, DLQ_SUBSCRIPTION_ID)

@app.get("/process-dlq")
def process_dlq():
    # Corrigir a chamada do método pull usando o objeto PullRequest
    response = subscriber.pull(request={"subscription": subscription_path, "max_messages": 10})
    messages = []

    for msg in response.received_messages:
        message_data = json.loads(msg.message.data.decode("utf-8"))
        messages.append(message_data)
        # Acknowledgment
        subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [msg.ack_id]})

    return {"messages": messages}

# Para rodar a API: uvicorn main:app --reload --port 8003
