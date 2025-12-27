"""
Exercise routes
"""
from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException, status
from bson import ObjectId

from app.db.client import MongoDBClient
from app.models.exercise import Exercise, ExercisePublic

router = APIRouter()


@router.get("/exercises", response_model=List[ExercisePublic])
async def get_exercises(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    """
    Get list of exercises
    
    Supports pagination with skip and limit parameters
    """
    db = MongoDBClient.get_database()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection not available",
        )
    
    cursor = db.exercises.find().skip(skip).limit(limit).sort("name", 1)
    exercises = []
    
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        exercises.append(ExercisePublic(**doc))
    
    return exercises


@router.get("/exercises/search", response_model=List[ExercisePublic])
async def search_exercises(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    """
    Search exercises by name, muscle group, or equipment
    
    Performs case-insensitive text search on name, primary_muscle, and equipment fields
    """
    db = MongoDBClient.get_database()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection not available",
        )
    
    # Create text search query (case-insensitive)
    search_query = {
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"primary_muscle": {"$regex": q, "$options": "i"}},
            {"equipment": {"$regex": q, "$options": "i"}},
        ]
    }
    
    cursor = db.exercises.find(search_query).skip(skip).limit(limit).sort("name", 1)
    exercises = []
    
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        exercises.append(ExercisePublic(**doc))
    
    return exercises

