from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated
from contextlib import asynccontextmanager
from database import create_tables, delete_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan)

class STaskAdd(BaseModel):
    name: str
    description: str|None = None

class STask(STaskAdd):
    id: int 


tasks = []

@app.post("/tasck")
async def add_task(
    task: Annotated[STaskAdd, Depends()]
):
    tasks.append(task)
    return {"ok": True}