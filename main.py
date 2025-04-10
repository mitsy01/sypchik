from fastapi import FastAPI,Path,Query,HTTPException,status
import uvicorn
from bs4 import BeautifulSoup
import re 
from aiohttp import ClientSession
import asyncio
from requests_html import HTMLSession,AsyncHTMLSession
import requests


app = FastAPI()

@app.get("/find/{tag}")
def find_text(
    tag: str = Path(..., description="div"),
    url: str = Query(..., description="https://uk.wikipedia.org/wiki/Наруто"),
    text: str = Query(..., description="За дванадцять років до початку основних подій серіалу демон Дев'ятихвостого Лиса (Кюбі) напав на Коноху (Селище Схованого Листа), що знаходиться в країні Вогню.")
):
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Сторінку не вдалося завантажити.")

    sypchik = BeautifulSoup(response.text, "html.parser")
    symbols = sypchik.find_all(tag)

    for symbol in symbols:
        full_text = symbol.get_text(strip=True)
        if re.search(re.escape(text), full_text):
            print(f"Текст: {full_text}")
            return {"found": full_text}

    print("Текст не знайдено")
    raise HTTPException(status_code=404, detail="Текст не знайдено")