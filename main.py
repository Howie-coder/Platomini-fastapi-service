from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
# import paddle
from paddle_chat import dialog_predict
import uvicore

class MessageInput(BaseModel):
    history: List[str]

class MessageOutput(BaseModel):
    response: str


app = FastAPI()

@app.get('/')
async def index() -> str:
    return 'OK'

@app.post('/messages')
async def respond_messages(input: MessageInput) -> MessageOutput:
    return MessageOutput(response=dialog_predict(input.history))

if __name__ == '__main__':
    uvicore.run(
        app=app,
        host="127.0.0.1",
        port=9001
    )