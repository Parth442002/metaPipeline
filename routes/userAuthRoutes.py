# userAuth.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

load_dotenv()
# Local Imports
from connectors.database import get_db
from utils.auth import *

router = APIRouter()

# Security
SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]


# ? Route to register a new user
@router.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    email = body.get("email")
    password = body.get("password")
    if get_user(db, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # Create a new user
    user = create_user(db, email, password)
    # Generate JWT token
    token_data = {"sub": user.email}
    token = create_jwt_token(token_data)

    return JSONResponse(
        content={
            "message": "User registered successfully",
            "user": jsonable_encoder(user),
            "access_token": token,
            "token_type": "bearer",
        },
        status_code=status.HTTP_201_CREATED,
    )


# ? Route for login
@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    email = body.get("email")
    password = body.get("password")
    user = get_user(db, email)
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token
    token_data = {"sub": user.email}
    token = create_jwt_token(token_data)

    return JSONResponse(
        content={
            "message": "Logged in successfully",
            "access_token": token,
            "user": jsonable_encoder(user),
            "token_type": "bearer",
        },
        status_code=status.HTTP_200_OK,
    )


# ? Protected route example
@router.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! You are logged in."}
