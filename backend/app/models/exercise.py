"""
Exercise model for MongoDB
"""
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict

from app.models.user import PyObjectId


# Expanded muscle groups
MUSCLE_GROUPS = [
    # Upper body
    "chest",
    "back",
    "shoulders",
    "biceps",
    "triceps",
    "forearms",
    "traps",
    # Lower body
    "quads",
    "hamstrings",
    "glutes",
    "calves",
    "abductors",
    "adductors",
    # Core
    "abs",
    "obliques",
    "lower_back",
    # Full body
    "full_body",
]

EQUIPMENT_TYPES = [
    "barbell",
    "dumbbell",
    "cable",
    "machine",
    "bodyweight",
    "kettlebell",
    "resistance_band",
    "medicine_ball",
    "other",
]

MOVEMENT_PATTERNS = [
    "push",
    "pull",
    "squat",
    "hinge",
    "lunge",
    "carry",
    "rotation",
    "isolation",
]

DIFFICULTY_LEVELS = [
    "beginner",
    "intermediate",
    "advanced",
]


class Exercise(BaseModel):
    """Exercise document model"""

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    primary_muscle: str  # Must be in MUSCLE_GROUPS
    secondary_muscles: List[str] = []  # List of muscles from MUSCLE_GROUPS
    equipment: str  # Must be in EQUIPMENT_TYPES
    movement_pattern: str  # Must be in MOVEMENT_PATTERNS
    difficulty: str  # Must be in DIFFICULTY_LEVELS
    notes: Optional[str] = None
    how_to_video_url: Optional[str] = None
    demo_media_url: Optional[str] = None  # For clip-art or drawn images
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Barbell Back Squat",
                "primary_muscle": "quads",
                "secondary_muscles": ["glutes", "hamstrings", "lower_back"],
                "equipment": "barbell",
                "movement_pattern": "squat",
                "difficulty": "intermediate",
                "notes": "Keep chest up, knees tracking over toes",
                "how_to_video_url": "https://example.com/squat-video",
            }
        },
    )

    def to_dict(self) -> dict:
        """Convert to dictionary for MongoDB"""
        data = self.model_dump(by_alias=True, exclude={"id"})
        data["_id"] = self.id
        return data


class ExercisePublic(BaseModel):
    """Public exercise model (for API responses)"""

    id: str
    name: str
    primary_muscle: str
    secondary_muscles: List[str]
    equipment: str
    movement_pattern: str
    difficulty: str
    notes: Optional[str] = None
    how_to_video_url: Optional[str] = None
    demo_media_url: Optional[str] = None

