from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL = "gemini-3.5-flash-lite"


def summarize(result: dict) -> str:
    """Az adatbázisból visszaolvasott eredményről 2-3 mondatos összefoglaló"""
    prompt = f"""
Foglald össze 2-3 mondatban, magyarul, közérthetően ennek az IP-címnek a biztonsági értékelését.
A verdict végleges, ne változtass rajta és ne vitasd. Csak a megadott adatokra támaszkodj, ne találj ki új információt.

IP-cím: {result["ip"]}
Verdict: {result["verdict"]}
VirusTotal statisztika: {result["stats"]}
"""
    client = genai.Client() 
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )
    return response.text