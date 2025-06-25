from fastapi import APIRouter, HTTPException, Depends
from auth import utils
from schemas.user import UserResponse, UserCreate
from db.session import get_db
from db.models import User

router = APIRouter(tags=['Users'])

@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db = Depends(get_db)):
    # Check if email already exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=utils.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user