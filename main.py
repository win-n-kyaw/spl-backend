from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.session import engine
from db.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

app = FastAPI()

