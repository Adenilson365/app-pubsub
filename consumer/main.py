from fastapi import FastAPI, Request, HTTPException
import json
import base64

app = FastAPI()

# Lista para armazenar mensagens aceitas
messages_storage = []

@app.post("/receive")
async def receive_message(request: Request):
    envelope = await request.json()
    message_data = envelope["message"]["data"]
    message = json.loads(base64.b64decode(message_data).decode("utf-8"))
    # Verifica se o campo isHuman é False
    if not message.get("isHuman", True):
        # Se isHuman for False, retorna um erro HTTP 400 para recusar a mensagem
        raise HTTPException(status_code=400, detail="Message rejected: isHuman is False")

    # Caso contrário, armazena a mensagem no array
    messages_storage.append(message)
    return {"status": "Message accepted", "message": message}

@app.get("/messages")
async def get_messages():
    # Retorna todas as mensagens armazenadas
    return {"stored_messages": messages_storage}

# Para rodar a API: uvicorn api_filter:app --reload --port 8002
