# IP-ellenőrző

Webalkalmazás, amely egy megadott IP címet a VirusTotal API-val ellenőriz, a statisztikából verdictet képez, az eredményt SQLite adatbázisba menti, majd a Google Gemini segítségével rövid  összefoglalót készít róla.

**Technológiák:** Python, FastAPI, SQLite, VirusTotal API, Google Gemini, pytest

## Futtatás

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # majd a saját API-kulcsok beírása
uvicorn main:app --reload
```

- Felület: http://127.0.0.1:8000
- API dokumentáció: http://127.0.0.1:8000/docs

## Tesztek

```
pytest -v
```