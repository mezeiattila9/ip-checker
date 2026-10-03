import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VT_API_KEY")
BASE_URL = "https://www.virustotal.com/api/v3/ip_addresses/"


def get_ip_stats(ip: str) -> dict:
    response = requests.get(
        BASE_URL + ip,
        headers={"x-apikey": API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["data"]["attributes"]["last_analysis_stats"]


def make_verdict(stats: dict) -> str:
    if stats.get("malicious", 0) > 0:
        return "malicious"
    if stats.get("suspicious", 0) > 0:
        return "suspicious"
    return "clean"