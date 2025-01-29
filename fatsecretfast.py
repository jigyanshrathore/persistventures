import httpx
import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# FatSecret API URLs
TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
API_URL = "https://platform.fatsecret.com/rest/server.api"

# Store access token globally
ACCESS_TOKEN = None


async def get_new_token():
    """Fetch a new OAuth 2.0 token from FatSecret."""
    global ACCESS_TOKEN
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    data = {"grant_type": "client_credentials"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, auth=(client_id, client_secret), data=data, headers=headers)

    if response.status_code == 200:
        ACCESS_TOKEN = response.json().get("access_token")
        return ACCESS_TOKEN
    else:
        raise HTTPException(status_code=400, detail="Failed to get access token")


@app.get("/")
async def home():
    """Default Route"""
    return {"message": "FastAPI FatSecret API Integration using OAuth 2.0"}


@app.get("/get_token")
async def fetch_token():
    """Manually fetch a new OAuth 2.0 token."""
    token = await get_new_token()
    return {"access_token": token}


@app.get("/search_foods")
async def search_foods(query: str):
    """Search for foods using FatSecret API with OAuth 2.0 authentication."""
    global ACCESS_TOKEN

    # Ensure we have a valid token
    if not ACCESS_TOKEN:
        ACCESS_TOKEN = await get_new_token()

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {
        "method": "foods.search",
        "format": "json",
        "search_expression": query
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:  # Token expired, refresh it
        ACCESS_TOKEN = await get_new_token()
        headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
        response = await client.get(API_URL, headers=headers, params=params)
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch food data")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
