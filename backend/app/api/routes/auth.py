"""
Authentication routes
"""
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from passlib.context import CryptContext
from bson import ObjectId

from app.core.config import settings
from app.core.security import create_access_token
from app.db.client import MongoDBClient
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """
    Register a new user
    
    Returns JWT token on successful registration
    """
    db = MongoDBClient.get_database()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection not available",
        )
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create new user
    user = User(
        email=request.email,
        password_hash=get_password_hash(request.password),
    )
    
    # Insert user
    result = await db.users.insert_one(user.to_dict())
    user.id = result.inserted_id
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=7),  # Longer expiry for registration
    )
    
    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Login user and return JWT token
    """
    db = MongoDBClient.get_database()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection not available",
        )
    
    # Find user
    user_doc = await db.users.find_one({"email": request.email})
    if user_doc is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(request.password, user_doc["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user_doc["_id"])},
        expires_delta=timedelta(days=7),
    )
    
    return TokenResponse(access_token=access_token)

