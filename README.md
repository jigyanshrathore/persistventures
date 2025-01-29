persistventures
 Step 1: Set Up Environment Variables
Create a .env file in the project directory.
Add the following credentials:
makefile
Copy
Edit
CLIENT_ID=your_fatsecret_client_id
CLIENT_SECRET=your_fatsecret_client_secret
Replace your_fatsecret_client_id and your_fatsecret_client_secret with your actual FatSecret API credentials.
🔹 Step 2: Start FastAPI Server
Run the FastAPI backend:

powershell
Copy
Edit
uvicorn fastapi_fatsecret:app --reload
Expected Output:

vbnet
Copy
Edit
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
🔹 Step 3: Get OAuth 2.0 Access Token
Run in PowerShell:
powershell
Copy
Edit
Invoke-RestMethod -Uri "http://127.0.0.1:8000/get_token"
✅ Expected Output:

json
Copy
Edit
{
  "access_token": "eyJhbGciOiJSUzI1NiIsImtpZ..."
}
🔹 Copy the full token (do not shorten it) for the next step.

🔹 Step 4: Fetch Food Data
Search for Food in PowerShell
Replace ACCESS_TOKEN_HERE with the full token received in Step 3:

powershell
Copy
Edit
$ACCESS_TOKEN="ACCESS_TOKEN_HERE"

Invoke-RestMethod -Uri "https://platform.fatsecret.com/rest/server.api?method=foods.search&format=json&search_expression=banana" `
-Headers @{"Authorization"="Bearer $ACCESS_TOKEN"} | ConvertTo-Json -Depth 3
✅ Expected JSON Response:

json
Copy
Edit
{
  "foods": {
    "food": [
      {
        "food_id": "12345",
        "food_name": "Banana",
        "food_description": "100g contains 89 calories, 0.3g fat, 22.8g carbs, 1.1g protein"
      }
    ]
  }
}
🔹 Step 5: Fetch More Results (Pagination)
To fetch additional results, modify the request:

powershell
Copy
Edit
Invoke-RestMethod -Uri "https://platform.fatsecret.com/rest/server.api?method=foods.search&format=json&search_expression=banana&page_number=1" `
-Headers @{"Authorization"="Bearer $ACCESS_TOKEN"} | ConvertTo-Json -Depth 3
🔹 This retrieves the second page of results.


powershell
Copy
Edit
uvicorn fastapi_fatsecret:app --reload --log-level debug
Check if .env file is missing or FatSecret credentials are incorrect.

2️⃣ If 401 Unauthorized Error Occurs
Run /get_token again to get a new access token.
Update the $ACCESS_TOKEN variable in PowerShell.
3️⃣ If 500 Internal Server Error
Restart FastAPI with:
powershell
Copy
Edit
uvicorn fastapi_fatsecret:app --reload
Check logs for errors.
