from ipaddress import IPv4Address

import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from database import init_db, save_result, get_latest_result
from virustotal import get_ip_stats, make_verdict
from llm import summarize

init_db()
app = FastAPI()


class IpRequest(BaseModel):
    ip: IPv4Address


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/api/check")
def check_ip(request: IpRequest):
    """VirusTotal, verdict, mentés, visszaolvasás, összefoglaló."""
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
    save_result(ip, verdict, stats)
    result = get_latest_result(ip)
    try:
        result["summary"] = summarize(result)
    except Exception as error:
        result["summary"] = None

    return result