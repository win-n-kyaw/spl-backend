from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from db.session import engine, Session
from db.models import Base, User
from auth.utils import hash_password
from auth.schemas import UserCreate, UserResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db = Depends(get_db)):
    # Check if email already exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

