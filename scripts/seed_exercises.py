#!/usr/bin/env python3
"""
Seed exercise library into MongoDB

Usage:
    python scripts/seed_exercises.py
"""
import asyncio
import json
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.client import MongoDBClient
from app.models.exercise import Exercise
from bson import ObjectId
from datetime import datetime


async def seed_exercises():
    """Seed exercises from JSON file into MongoDB"""
    # Connect to database
    await MongoDBClient.connect()
    db = MongoDBClient.get_database()
    
    if db is None:
        print("ERROR: Database connection not available")
        return
    
    # Load exercises from JSON
    exercises_file = Path(__file__).parent.parent / "backend" / "app" / "data" / "exercises.json"
    
    if not exercises_file.exists():
        print(f"ERROR: Exercises file not found at {exercises_file}")
        return
    
    with open(exercises_file, "r") as f:
        exercises_data = json.load(f)
    
    print(f"Loading {len(exercises_data)} exercises from {exercises_file}")
    
    inserted_count = 0
    updated_count = 0
    
    for exercise_data in exercises_data:
        try:
            # Create exercise model
            exercise = Exercise(**exercise_data)
            
            # Check if exercise already exists (by name)
            existing = await db.exercises.find_one({"name": exercise.name})
            
            if existing:
                # Update existing exercise
                update_data = exercise.model_dump(by_alias=True, exclude={"id", "created_at"})
                update_data["updated_at"] = datetime.utcnow()
                
                await db.exercises.update_one(
                    {"_id": existing["_id"]},
                    {"$set": update_data}
                )
                updated_count += 1
                print(f"  Updated: {exercise.name}")
            else:
                # Insert new exercise
                exercise_dict = exercise.to_dict()
                await db.exercises.insert_one(exercise_dict)
                inserted_count += 1
                print(f"  Inserted: {exercise.name}")
                
        except Exception as e:
            print(f"  ERROR processing {exercise_data.get('name', 'unknown')}: {e}")
    
    print(f"\nCompleted!")
    print(f"  Inserted: {inserted_count} exercises")
    print(f"  Updated: {updated_count} exercises")
    print(f"  Total: {inserted_count + updated_count} exercises")
    
    # Disconnect
    await MongoDBClient.disconnect()


if __name__ == "__main__":
    asyncio.run(seed_exercises())

