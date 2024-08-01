from fastapi import FastAPI, status, Body, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

class Message(BaseModel):
    age: int = None
    text: str
    id: int = None

@app.get('/')
def get_all_messages() -> List[Message]:
    return users

@app.get(path = "/user/{user_id}")
def get_message(user_id: int) -> Message:
    try:
        return users[user_id]
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

@app.post('/user')
def create_message(user: Message) -> str:
    user.id = len(users)
    users.append(user)
    return f'message created'

@app.put("/user/{user_id}/{username}/{age}")
def update_message(user_id: int, user: str = Body()) -> str:
    try:
        edit_message = users[user_id]
        edit_message.text = user
        return f'Message updated'
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

@app.delete("/user/{user_id}")
def delete_message(user_id: int) -> str:
    try:
        users.pop(user_id)
        return f"Message ID = {user_id} deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

@app.delete("/")
def kill_messages_all() -> str:
    users.clear()
    return 'All Messages deleted'


