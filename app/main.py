from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from app.db import fetch_clients, fetch_users, initialize_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(lifespan=lifespan)


class Client(BaseModel):
    id: int
    name: str
    email: str


class User(BaseModel):
    id: int
    name: str
    email: str

@app.get("/clients", response_model=list[Client])
def list_clients() -> list[Client]:
    return [Client(**client) for client in fetch_clients()]


@app.get("/users", response_model=list[User])
def list_users() -> list[User]:
    return [User(**user) for user in fetch_users()]
