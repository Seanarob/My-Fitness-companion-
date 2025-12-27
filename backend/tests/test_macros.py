"""
Tests for macro calculation module
"""
import pytest
from app.services.macros import calculate_macros


def test_macro_calculation_lean_bulk_205lb():
    """
    Test macro calculation for a 205 lb male doing lean bulk
    Should target ~205-210g protein for muscle building
    """
    result = calculate_macros(
        weight_lbs=205.0,
        height_inches=72,  # 6 feet
        age=28,
        is_male=True,
        goal="build_muscle",
        training_days_per_week=5
    )
    
    # Check protein is in target range for muscle building (1.2g/lb = ~246g for 205lbs)
    # Standard range for muscle building is 1.2-1.6g/lb, so 205-330g is acceptable
    assert 205 <= result["protein_g"] <= 330, f"Protein {result['protein_g']}g not in expected range for muscle building (205-330g)"
    
    # Check calories are positive and reasonable (surplus for muscle building)
    assert result["calories"] > 2500, "Calories should be substantial for 205lb male"
    
    # Check all macros are positive
    assert result["protein_g"] > 0
    assert result["carbs_g"] > 0
    assert result["fat_g"] > 0
    
    # Check fat is within 20-30% of calories
    fat_calories = result["fat_g"] * 9
    fat_percent = (fat_calories / result["calories"]) * 100
    assert 20 <= fat_percent <= 30, f"Fat {fat_percent:.1f}% not in range 20-30%"
    
    # Check fat meets minimum 0.3g per lb
    fat_min = 205 * 0.3
    assert result["fat_g"] >= fat_min, f"Fat {result['fat_g']}g below minimum {fat_min}g"
    
    # Verify total calories match
    total_calc = (result["protein_g"] * 4) + (result["carbs_g"] * 4) + (result["fat_g"] * 9)
    assert abs(total_calc - result["calories"]) < 10, "Total calculated calories don't match"


def test_macro_calculation_weight_loss():
    """
    Test macro calculation for weight loss goal
    Should have calorie deficit and adequate protein
    """
    result = calculate_macros(
        weight_lbs=180.0,
        height_inches=70,  # 5'10"
        age=35,
        is_male=True,
        goal="lose_weight",
        training_days_per_week=4
    )
    
    # Protein should be ~1.0g per lb for weight loss (180g)
    assert 175 <= result["protein_g"] <= 185, f"Protein {result['protein_g']}g not around 180g"
    
    # Calories should be reasonable for weight loss
    assert result["calories"] > 1500, "Calories too low"
    assert result["calories"] < 3000, "Calories too high for weight loss"
    
    # All macros positive
    assert result["protein_g"] > 0
    assert result["carbs_g"] >= 0  # Can be low for weight loss
    assert result["fat_g"] > 0
    
    # Fat should meet minimum
    fat_min = 180 * 0.3
    assert result["fat_g"] >= fat_min, "Fat below minimum"


def test_macro_calculation_maintenance_female():
    """
    Test macro calculation for maintenance goal (female)
    """
    result = calculate_macros(
        weight_lbs=140.0,
        height_inches=65,  # 5'5"
        age=30,
        is_male=False,
        goal="maintain",
        training_days_per_week=3
    )
    
    # Protein should be ~0.8g per lb (112g)
    assert 100 <= result["protein_g"] <= 120, f"Protein {result['protein_g']}g not around 112g"
    
    # Calories should be reasonable for maintenance
    assert result["calories"] > 1500, "Calories too low"
    assert result["calories"] < 2500, "Calories too high for maintenance"
    
    # All macros positive
    assert result["protein_g"] > 0
    assert result["carbs_g"] > 0
    assert result["fat_g"] > 0
    
    # Fat should meet minimum 0.3g per lb (42g)
    fat_min = 140 * 0.3
    assert result["fat_g"] >= fat_min, "Fat below minimum"
    
    # Verify macro split adds up
    total_calc = (result["protein_g"] * 4) + (result["carbs_g"] * 4) + (result["fat_g"] * 9)
    assert abs(total_calc - result["calories"]) < 10, "Total calculated calories don't match"

