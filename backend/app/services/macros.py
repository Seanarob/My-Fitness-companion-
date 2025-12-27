"""
Macro calculation module using Mifflin-St Jeor equation
"""
from typing import Dict

# Constants
# Activity multipliers (BMR multipliers)
ACTIVITY_SEDENTARY = 1.2  # Little to no exercise
ACTIVITY_LIGHT = 1.375  # Light exercise 1-3 days/week
ACTIVITY_MODERATE = 1.55  # Moderate exercise 3-5 days/week
ACTIVITY_ACTIVE = 1.725  # Hard exercise 6-7 days/week
ACTIVITY_VERY_ACTIVE = 1.9  # Very hard exercise, physical job

# Goal adjustments (calorie multipliers)
GOAL_LOSE_WEIGHT = -0.20  # 20% deficit
GOAL_BUILD_MUSCLE = 0.10  # 10% surplus
GOAL_MAINTAIN = 0.0  # Maintenance
GOAL_IMPROVE_ENDURANCE = 0.05  # 5% surplus
GOAL_GENERAL_FITNESS = 0.0  # Maintenance

# Protein ranges (g per lb bodyweight)
PROTEIN_MIN = 0.8  # Minimum for general health
PROTEIN_MAINTENANCE = 0.8
PROTEIN_LOSE_WEIGHT = 1.0
PROTEIN_BUILD_MUSCLE = 1.2  # 1.2-1.6g per lb for muscle building
PROTEIN_ENDURANCE = 0.9
PROTEIN_GENERAL = 0.8

# Fat constants
FAT_PERCENT_MIN = 0.20  # Minimum 20% of calories
FAT_PERCENT_MAX = 0.30  # Maximum 30% of calories
FAT_MIN_PER_LB = 0.3  # Minimum 0.3g per lb bodyweight

# Calories per gram
CALORIES_PER_GRAM_PROTEIN = 4
CALORIES_PER_GRAM_CARB = 4
CALORIES_PER_GRAM_FAT = 9


def calculate_bmr_mifflin_st_jeor(
    weight_lbs: float,
    height_inches: int,
    age: int,
    is_male: bool
) -> float:
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor equation
    
    Args:
        weight_lbs: Weight in pounds
        height_inches: Height in inches
        age: Age in years
        is_male: True for male, False for female
        
    Returns:
        BMR in calories per day
    """
    weight_kg = weight_lbs * 0.453592
    height_cm = height_inches * 2.54
    
    if is_male:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    
    return bmr


def get_activity_multiplier(training_days_per_week: int) -> float:
    """
    Get activity multiplier based on training days per week
    
    Args:
        training_days_per_week: Number of training days (1-7)
        
    Returns:
        Activity multiplier
    """
    if training_days_per_week == 0:
        return ACTIVITY_SEDENTARY
    elif training_days_per_week <= 2:
        return ACTIVITY_LIGHT
    elif training_days_per_week <= 4:
        return ACTIVITY_MODERATE
    elif training_days_per_week <= 6:
        return ACTIVITY_ACTIVE
    else:
        return ACTIVITY_VERY_ACTIVE


def get_goal_adjustment(goal: str) -> float:
    """
    Get calorie adjustment multiplier based on goal
    
    Args:
        goal: Goal string (lose_weight, build_muscle, etc.)
        
    Returns:
        Goal adjustment multiplier (e.g., -0.20 for 20% deficit)
    """
    goal_map = {
        "lose_weight": GOAL_LOSE_WEIGHT,
        "build_muscle": GOAL_BUILD_MUSCLE,
        "maintain": GOAL_MAINTAIN,
        "improve_endurance": GOAL_IMPROVE_ENDURANCE,
        "general_fitness": GOAL_GENERAL_FITNESS,
    }
    return goal_map.get(goal, GOAL_MAINTAIN)


def get_protein_per_lb(goal: str) -> float:
    """
    Get protein requirement per pound of bodyweight based on goal
    
    Args:
        goal: Goal string
        
    Returns:
        Protein grams per pound of bodyweight
    """
    goal_map = {
        "lose_weight": PROTEIN_LOSE_WEIGHT,
        "build_muscle": PROTEIN_BUILD_MUSCLE,
        "maintain": PROTEIN_MAINTENANCE,
        "improve_endurance": PROTEIN_ENDURANCE,
        "general_fitness": PROTEIN_GENERAL,
    }
    return goal_map.get(goal, PROTEIN_MIN)


def calculate_macros(
    weight_lbs: float,
    height_inches: int,
    age: int,
    is_male: bool,
    goal: str,
    training_days_per_week: int
) -> Dict[str, float]:
    """
    Calculate daily macronutrient targets
    
    Steps:
    1. Calculate BMR using Mifflin-St Jeor
    2. Multiply by activity multiplier to get maintenance calories
    3. Adjust by goal (deficit/surplus)
    4. Set protein based on bodyweight and goal
    5. Set fat at 20-30% of calories with minimum 0.3g per lb
    6. Fill remaining calories with carbs
    
    Args:
        weight_lbs: Weight in pounds
        height_inches: Height in inches
        age: Age in years
        is_male: True for male, False for female
        goal: Goal string (lose_weight, build_muscle, etc.)
        training_days_per_week: Number of training days per week
        
    Returns:
        Dictionary with calories, protein_g, carbs_g, fat_g
    """
    # Step 1: Calculate BMR
    bmr = calculate_bmr_mifflin_st_jeor(weight_lbs, height_inches, age, is_male)
    
    # Step 2: Apply activity multiplier to get maintenance
    activity_mult = get_activity_multiplier(training_days_per_week)
    maintenance_calories = bmr * activity_mult
    
    # Step 3: Apply goal adjustment
    goal_adj = get_goal_adjustment(goal)
    target_calories = maintenance_calories * (1 + goal_adj)
    
    # Step 4: Calculate protein
    protein_per_lb = get_protein_per_lb(goal)
    protein_g = weight_lbs * protein_per_lb
    protein_calories = protein_g * CALORIES_PER_GRAM_PROTEIN
    
    # Step 5: Calculate fat (20-30% of calories, minimum 0.3g per lb)
    fat_min_g = weight_lbs * FAT_MIN_PER_LB
    fat_min_calories = fat_min_g * CALORIES_PER_GRAM_FAT
    
    fat_max_calories = target_calories * FAT_PERCENT_MAX
    fat_min_calories_from_percent = target_calories * FAT_PERCENT_MIN
    
    # Use the higher of minimums (either 0.3g/lb or 20% of calories)
    fat_target_calories = max(fat_min_calories, fat_min_calories_from_percent)
    # Don't exceed 30% of calories
    fat_target_calories = min(fat_target_calories, fat_max_calories)
    
    fat_g = fat_target_calories / CALORIES_PER_GRAM_FAT
    fat_calories = fat_g * CALORIES_PER_GRAM_FAT
    
    # Step 6: Fill remaining calories with carbs
    remaining_calories = target_calories - protein_calories - fat_calories
    carbs_g = remaining_calories / CALORIES_PER_GRAM_CARB
    
    # Ensure carbs are non-negative
    if carbs_g < 0:
        carbs_g = 0
        # Adjust fat if needed
        fat_calories = target_calories - protein_calories
        fat_g = fat_calories / CALORIES_PER_GRAM_FAT
    
    return {
        "calories": round(target_calories),
        "protein_g": round(protein_g, 1),
        "carbs_g": round(carbs_g, 1),
        "fat_g": round(fat_g, 1),
    }

