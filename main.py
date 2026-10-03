from ipaddress import IPv4Address
from virustotal import get_ip_stats, make_verdict
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import request
app = FastAPI()


class IpRequest(BaseModel):
    ip: IPv4Address


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/api/check")
def check_ip(request: IpRequest):
    ip = str(request.ip)

    try:
        stats = get_ip_stats(ip)
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="A VirusTotal nem válaszolt időben.")
    except requests.exceptions.HTTPError as error:
        status = error.response.status_code
        if status == 429:
            raise HTTPException(status_code=429, detail="Túl sok kérés, próbáld újra egy perc múlva.")
        if status == 401:
            raise HTTPException(status_code=502, detail="Hibás VirusTotal API-kulcs.")
        raise HTTPException(status_code=502, detail="Hiba a VirusTotal lekérdezésekor.")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=502, detail="A VirusTotal nem érhető el.")

    verdict = make_verdict(stats)
    return {"ip": ip, "verdict": verdict, "stats": stats}