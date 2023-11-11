from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from models.userModel import UserModel
import jwt
from jose import JWTError
import os
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]


def create_user(db: Session, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = UserModel(email=email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Function to get a user by email
def get_user(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


# Function to create JWT token
def create_jwt_token(data: dict):
    expiration_time = datetime.utcnow() + timedelta(hours=1)  # Set expiration to 1 hour
    data["exp"] = expiration_time
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Remove "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token[len("Bearer ") :]

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        expiration_time = payload.get("exp")
        # Check if the token has expired
        if (
            expiration_time is not None
            and datetime.utcnow() > datetime.utcfromtimestamp(expiration_time)
        ):
            raise credentials_exception

        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception
