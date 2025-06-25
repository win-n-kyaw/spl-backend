from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from db.session import engine
from db.models import Base, User
from routes.auth import router as auth_router
from auth import jwt
from routes.user import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/protected")
def protected(current_user: User = Depends(jwt.get_current_user)):
    # print(current_user.email)
    return "Congrats..."

