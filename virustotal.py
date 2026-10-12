import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VT_API_KEY")
BASE_URL = "https://www.virustotal.com/api/v3/ip_addresses/"


def get_ip_stats(ip: str) -> dict:
        """Lekéri a VirusTotalról az IP cím statisztikáját"""
    response = requests.get(
        BASE_URL + ip,
        headers={"x-apikey": API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["data"]["attributes"]["last_analysis_stats"]


MALICIOUS_THRESHOLD = 0.02
SUSPICIOUS_THRESHOLD = 0.05


def make_verdict(stats: dict) -> str:
        """Az statisztikából verdictet képez: clean, suspicious, malicious vagy unknown."""
    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)
    total = (
        malicious
        + suspicious
        + stats.get("harmless", 0)
        + stats.get("undetected", 0)
    )

    if total == 0:
        return "unknown"
    if malicious / total >= MALICIOUS_THRESHOLD:
        return "malicious"
    if (malicious + suspicious) / total >= SUSPICIOUS_THRESHOLD:
        return "suspicious"
    return "clean"