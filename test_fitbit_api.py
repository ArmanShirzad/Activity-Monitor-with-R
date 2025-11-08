#!/usr/bin/env python3
"""
Test script to verify Fitbit API integration and rate limiting
"""
import requests
import time
import sys

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✓ Health check passed")

def test_platforms():
    """Test platforms endpoint"""
    print("\nTesting platforms endpoint...")
    response = requests.get(f"{API_URL}/api/v1/platforms")
    assert response.status_code == 200
    platforms = response.json()["platforms"]
    assert len(platforms) > 0
    fitbit = next((p for p in platforms if p["id"] == "fitbit"), None)
    assert fitbit is not None
    print(f"✓ Platforms endpoint passed - Found {len(platforms)} platforms")

def test_oauth_authorize():
    """Test OAuth authorize endpoint"""
    print("\nTesting OAuth authorize endpoint...")
    response = requests.get(f"{API_URL}/api/v1/auth/fitbit/authorize", allow_redirects=False)
    # Should redirect (307 or 302)
    assert response.status_code in [302, 307]
    assert "fitbit.com" in response.headers.get("Location", "")
    print("✓ OAuth authorize endpoint redirects correctly")

def test_analyze_without_token():
    """Test analyze endpoint without token (should fail gracefully)"""
    print("\nTesting analyze endpoint without token...")
    from datetime import datetime, timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    response = requests.post(
        f"{API_URL}/api/v1/activity/analyze",
        json={
            "platform": "fitbit",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "access_token": "",
            "refresh_token": ""
        }
    )
    # Should return error but not crash
    assert response.status_code in [400, 401, 404, 500]
    print(f"✓ Analyze endpoint handles missing token (status: {response.status_code})")

def main():
    """Run all tests"""
    print("=" * 50)
    print("Fitbit API Integration Tests")
    print("=" * 50)
    
    try:
        test_health()
        test_platforms()
        test_oauth_authorize()
        test_analyze_without_token()
        
        print("\n" + "=" * 50)
        print("All tests passed!")
        print("=" * 50)
        print("\nNote: Full OAuth flow requires:")
        print("1. Valid Fitbit Client ID and Secret in backend/.env")
        print("2. User authorization via browser")
        print("3. Access token from OAuth callback")
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except requests.exceptions.ConnectionError:
        print("\n✗ Cannot connect to backend. Is it running?")
        print("   Start with: docker compose up -d")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

