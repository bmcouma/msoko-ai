import requests
import json

base_url = "http://127.0.0.1:8000/api/auth/"

def test_registration():
    url = base_url + "register/"
    data = {
        "first_name": "Antigravity",
        "last_name": "Test",
        "email": "test@antigravity.ai",
        "password": "professional_password_123",
        "confirm_password": "professional_password_123"
    }
    response = requests.post(url, json=data)
    print(f"Registration Status: {response.status_code}")
    print(f"Registration Response: {response.json()}")
    return response.status_code == 200

def test_login():
    url = base_url + "login/"
    data = {
        "email": "test@antigravity.ai",
        "password": "professional_password_123"
    }
    response = requests.post(url, json=data)
    print(f"Login Status: {response.status_code}")
    print(f"Login Response: {response.json()}")

if __name__ == "__main__":
    if test_registration():
        test_login()
