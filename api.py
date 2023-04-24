from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Pydantic数据规范定义
class MessageInput(BaseModel):
    history: List[str]

class MessageOutput(BaseModel):
    response: str
# Pydantic数据规范定义结束

class ChatAgentAPI():
    def __init__(self,dialog_predict_func) -> None:
        self.dialog_predict_func = dialog_predict_func
    def run(self,port) -> str:
        # FastAPI接口定义
        app = FastAPI()          
        @app.get('/')
        async def index() -> str:
            return 'plato service running...' 
        @app.post('/messages')
        async def respond_messages(input: MessageInput) -> MessageOutput:
            return MessageOutput(response=self.dialog_predict_func(input.history))
        # FastAPI接口定义结束

        uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=port,
        )
    
