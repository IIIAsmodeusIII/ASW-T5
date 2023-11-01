import json
from fastapi import FastAPI, Response
app = FastAPI()

## Server ##
USERS = json.load(open("app/response.json"))

@app.get("/users/")
def read_root():
    return {"users": USERS}

@app.get("/users/{id}") 
def findUser(id: str):
    for _, user in USERS.items():
        if user["userId"] == id:
            return user