from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Customer(BaseModel):
    id: int
    name: str
    email: str


CUSTOMERS = [
    Customer(id=1, name="Ada Lovelace", email="ada.lovelace@example.com"),
    Customer(id=2, name="Grace Hopper", email="grace.hopper@example.com"),
    Customer(id=3, name="Alan Turing", email="alan.turing@example.com"),
]


@app.get("/customers", response_model=list[Customer])
def list_customers() -> list[Customer]:
    return CUSTOMERS
