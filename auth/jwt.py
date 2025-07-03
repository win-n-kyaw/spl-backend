from datetime import datetime, timedelta
from auth import config
from jose import JWTError, jwt
from schemas.token import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from db import session, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    if not config.SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in config and cannot be None")

    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, config.ALOGRITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        if not config.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set in config and cannot be None")
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALOGRITHM])
        id_ = payload.get("user_id")
        if id_ is None:
            raise credentials_exception
        token_data = TokenData(id=str(id_))
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(session.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.Admin).filter(models.Admin.id == token_data.id).first()
    if not user:
        raise credentials_exception
    return user
