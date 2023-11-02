import json
from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()

## Server ##
USERS = json.load(open("app/response.json"))

class Logger(BaseModel):
    username: str
    password: str

@app.post("/login/")
def read_root(data: Logger):
    for user, password in USERS.items():
        if data.username == user[0] and data.password == password[0]:
            return {"token": user[1]}
    return {"token": "-1"}
