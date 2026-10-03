from ipaddress import IPv4Address

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()


class IpRequest(BaseModel):
    ip: IPv4Address


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/api/check")
def check_ip(request: IpRequest):
    return {"ip": str(request.ip), "status": "ok"}