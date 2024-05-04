import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Form, Header
import requests
from keycloak import KeycloakOpenID

app = FastAPI()

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                 client_id=KEYCLOAK_CLIENT_ID,
                                 realm_name=KEYCLOAK_REALM,
                                 client_secret_key=KEYCLOAK_CLIENT_SECRET)


@app.post("/sign_in")
async def sign_in(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")


def check_for_role(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive(token: str = Header()):
    if (check_for_role(token)):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.get("/get_popular_memes")
async def get_popular_memes(token: str = Header()):
    if (check_for_role(token)):
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
    else:
        return "Wrong JWT Token"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
