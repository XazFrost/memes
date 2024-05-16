import uvicorn
from fastapi import FastAPI, HTTPException, status
import requests

app = FastAPI()

@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'Service alive'}



@app.get("/get_popular_memes")
async def get_popular_memes():
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            return data["data"]["memes"]
        else:
            raise HTTPException(status_code=400, detail="Error retrieving popular memes")
    else:
        raise HTTPException(status_code=response.status_code, detail="Error contacting Imgflip API")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
