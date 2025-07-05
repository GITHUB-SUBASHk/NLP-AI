import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from ai.assistant_engine.ai_router import route_message

active_connections = {}

async def connect(websocket: WebSocket, sender_id: str, receiver_id: str):
    await websocket.accept()
    active_connections[(sender_id, receiver_id)] = websocket

async def disconnect(sender_id: str, receiver_id: str):
    active_connections.pop((sender_id, receiver_id), None)

async def send_personal_message(message: str, sender_id: str, receiver_id: str):
    ws = active_connections.get((sender_id, receiver_id))
    if ws:
        await ws.send_text(message)

async def receive_and_reply(websocket: WebSocket, user_id: str):
    try:
        while True:
            data = await websocket.receive_text()
            reply = route_message(data)
            await websocket.send_text(json.dumps({"reply": reply}))
    except WebSocketDisconnect:
        await disconnect_user(user_id)