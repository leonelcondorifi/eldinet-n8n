from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Customer(BaseModel):
    id: int
    name: str
    email: str


class User(BaseModel):
    id: int
    name: str
    email: str


CUSTOMERS = [
    Customer(id=1, name="Ada Lovelace", email="ada.lovelace@example.com"),
    Customer(id=2, name="Grace Hopper", email="grace.hopper@example.com"),
    Customer(id=3, name="Alan Turing", email="alan.turing@example.com"),
]

USERS = [
    User(id=1, name="Katherine Johnson", email="katherine.johnson@example.com"),
    User(id=2, name="Margaret Hamilton", email="margaret.hamilton@example.com"),
    User(id=3, name="Edsger Dijkstra", email="edsger.dijkstra@example.com"),
]


@app.get("/customers", response_model=list[Customer])
def list_customers() -> list[Customer]:
    return CUSTOMERS


@app.get("/users", response_model=list[User])
def list_users() -> list[User]:
    return USERS
