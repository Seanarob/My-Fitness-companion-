"""
User routes including onboarding
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId

from app.core.dependencies import get_current_user
from app.db.client import MongoDBClient
from app.models.user import User, UserProfile, MacroTargets, UserPublic
from app.services.macros import calculate_macros

router = APIRouter()


class OnboardingRequest(BaseModel):
    """Onboarding request model"""
    
    goal: str
    experience: str
    training_days_per_week: int
    equipment_style: str
    check_in_day: str
    height_feet: int
    height_inches: int
    weight_pounds: float
    age: int
    gender: Optional[str] = None
    food_preferences: List[str]
    allergies: List[str]
    meals_per_day: int
    wake_time: Optional[str] = None
    sleep_time: Optional[str] = None
    injuries: List[str]
    budget_tier: str
    current_cardio: str
    motivation_style: str


@router.post("/onboarding", response_model=UserPublic)
async def submit_onboarding(
    request: OnboardingRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Submit user onboarding data
    
    Requires authentication. Calculates macros and stores user profile.
    """
    db = MongoDBClient.get_database()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection not available",
        )
    
    # Create user profile
    profile = UserProfile(**request.model_dump())
    
    # Calculate macros
    total_height_inches = (request.height_feet * 12) + request.height_inches
    is_male = request.gender == "male"
    
    macro_result = calculate_macros(
        weight_lbs=request.weight_pounds,
        height_inches=total_height_inches,
        age=request.age,
        is_male=is_male,
        goal=request.goal,
        training_days_per_week=request.training_days_per_week,
    )
    
    macro_targets = MacroTargets(
        calories=macro_result["calories"],
        protein_g=macro_result["protein_g"],
        carbs_g=macro_result["carbs_g"],
        fat_g=macro_result["fat_g"],
        updated_at=datetime.utcnow(),
    )
    
    # Update user in database
    update_data = {
        "profile": profile.model_dump(),
        "macro_targets": macro_targets.model_dump(),
        "macros_can_change_weekly": True,  # Reminder field
        "updated_at": datetime.utcnow(),
    }
    
    # Convert user id to ObjectId if needed
    user_object_id = current_user.id if isinstance(current_user.id, ObjectId) else ObjectId(str(current_user.id))
    
    await db.users.update_one(
        {"_id": user_object_id},
        {"$set": update_data}
    )
    
    # Fetch updated user
    updated_user_doc = await db.users.find_one({"_id": user_object_id})
    if updated_user_doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found after update",
        )
    
    # Return public user profile
    updated_user = User(**updated_user_doc)
    return UserPublic(
        id=str(updated_user.id),
        email=updated_user.email,
        profile=updated_user.profile,
        macro_targets=updated_user.macro_targets,
        macros_can_change_weekly=updated_user.macros_can_change_weekly,
    )

