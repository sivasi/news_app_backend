from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# making the instance of FastAPI framework
app = FastAPI()

# adding the cors options
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# gettig the api key
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# making the routes for giving response
@app.get("/search")
async def search_news(name: str = Query(..., min_length=1)):
    url = "https://google.serper.dev/news"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": name,
        "gl": "in"
    }

    try: 
        # calling the serper api
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                
                # return only news array response of serper api 
                return response.json()['news']
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=str(e))
