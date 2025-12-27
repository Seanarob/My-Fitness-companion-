"""
Tests for authentication and protected endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_protected_endpoint_without_token():
    """Test that protected endpoint returns 401 without token"""
    response = client.post("/api/v1/users/onboarding", json={
        "goal": "build_muscle",
        "experience": "intermediate",
        "training_days_per_week": 4,
        "equipment_style": "full_gym",
        "check_in_day": "monday",
        "height_feet": 6,
        "height_inches": 0,
        "weight_pounds": 180.0,
        "age": 30,
        "gender": "male",
        "food_preferences": ["high_protein"],
        "allergies": [],
        "meals_per_day": 4,
        "wake_time": None,
        "sleep_time": None,
        "injuries": [],
        "budget_tier": "moderate",
        "current_cardio": "Running 3x/week",
        "motivation_style": "supportive",
    })
    
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_protected_endpoint_with_token():
    """Test that protected endpoint returns 200 with valid token"""
    # First register a user to get a token
    register_response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "testpassword123",
    })
    
    assert register_response.status_code == 201
    token_data = register_response.json()
    assert "access_token" in token_data
    access_token = token_data["access_token"]
    
    # Now try the protected endpoint with token
    response = client.post(
        "/api/v1/users/onboarding",
        json={
            "goal": "build_muscle",
            "experience": "intermediate",
            "training_days_per_week": 4,
            "equipment_style": "full_gym",
            "check_in_day": "monday",
            "height_feet": 6,
            "height_inches": 0,
            "weight_pounds": 180.0,
            "age": 30,
            "gender": "male",
            "food_preferences": ["high_protein"],
            "allergies": [],
            "meals_per_day": 4,
            "wake_time": None,
            "sleep_time": None,
            "injuries": [],
            "budget_tier": "moderate",
            "current_cardio": "Running 3x/week",
            "motivation_style": "supportive",
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    # Should succeed (200) if endpoint is implemented, or 422 if validation fails
    # But should NOT be 401 (unauthorized)
    assert response.status_code != 401
    assert response.status_code in [200, 422]  # 422 for validation errors is ok


def test_public_endpoints_accessible():
    """Test that public endpoints are accessible without auth"""
    # Health check
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    # Register endpoint
    response = client.post("/api/v1/auth/register", json={
        "email": "public@example.com",
        "password": "password123",
    })
    assert response.status_code in [201, 400]  # 400 if already exists is ok
    
    # Login endpoint
    response = client.post("/api/v1/auth/login", json={
        "email": "public@example.com",
        "password": "password123",
    })
    # May be 401 if user doesn't exist, but endpoint is accessible (not 404)
    assert response.status_code != 404

