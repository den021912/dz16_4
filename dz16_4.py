from fastapi import FastAPI, status, Body, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []

class User(BaseModel):
    age: int
    username: str
    id: int

@app.get('/')
async def get_all_user() -> List[User]:
    return users

@app.get(path = "/user/{user_id}")
async def get_user(user_id: int) -> User:
    try:
        return users[user_id]
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

@app.post('/user/{username}/{age}')
async def create_user(username: str, age: int) -> User:
    user_id = max(users, key=lambda x: int(x.id)).id + 1 if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int, username: str, age: int) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> str:
    try:
        users.pop(user_id)
        return f"User ID = {user_id} deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

@app.delete("/")
async def kill_user_all() -> str:
    users.clear()
    return 'All deleted'


