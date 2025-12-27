"""
User model for MongoDB
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict


class PyObjectId(ObjectId):
    """Custom ObjectId for Pydantic v2"""
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.with_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.str_schema(),
        )
    
    @classmethod
    def validate(cls, v, handler=None):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            return ObjectId(v)
        raise ValueError("Invalid ObjectId type")


class MacroTargets(BaseModel):
    """Macro targets for user"""

    calories: int
    protein_g: float
    carbs_g: float
    fat_g: float
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserProfile(BaseModel):
    """User profile data"""

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
    food_preferences: List[str] = []
    allergies: List[str] = []
    meals_per_day: int
    wake_time: Optional[str] = None
    sleep_time: Optional[str] = None
    injuries: List[str] = []
    budget_tier: str
    current_cardio: str
    motivation_style: str


class User(BaseModel):
    """User document model"""

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    password_hash: str
    profile: Optional[UserProfile] = None
    macro_targets: Optional[MacroTargets] = None
    macros_can_change_weekly: bool = True  # Reminder that macros can change weekly
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "profile": {
                    "goal": "build_muscle",
                    "experience": "intermediate",
                    "training_days_per_week": 4,
                },
            }
        },
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MongoDB"""
        data = self.model_dump(by_alias=True, exclude={"id"})
        data["_id"] = self.id
        return data


class UserPublic(BaseModel):
    """Public user profile (no sensitive data)"""

    id: str
    email: str
    profile: Optional[UserProfile] = None
    macro_targets: Optional[MacroTargets] = None
    macros_can_change_weekly: bool = True

