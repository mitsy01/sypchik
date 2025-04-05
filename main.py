import re

from bs4 import BeautifulSoup
from aiohttp import ClientSession
import asyncio
from requests_html import HTMLSession, AsyncHTMLSession
from fastapi import FastAPI, Path, Query, HTTPException, status
from fastapi.responses import JSONResponse

async def fetch_url_with_aiohttp(url: str) -> str:
    async with ClientSession() as session:
        response = await session.get(url, verify=False)
        if response.status == 200:
            return await  response.text(encoding="utf-8")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
   
   
def fetch_url_requestes_html(url: str) -> str:
    session = HTMLSession()
    responce =  session.get(url)
    if responce.status_code == 200:
        return responce.text
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    

url = "https://uk.wikipedia.org/wiki/Наруто"
tag = "div"
found_text = "Під час цього турніру на Коноху нападає Орочімару — злочинець класу S. "

html = fetch_url_requestes_html(url)
# html = asyncio.run(fetch_url_with_aiohttp(url))
soup = BeautifulSoup(html, "lxml")
text = soup.find(string=re.compile(found_text)).find_parent(tag)

if text:
    print("text=", text.text)
    print("gettext=", text.get_text())
else:
    print("not found")

print(html)
    
    
# html = asyncio.run(fetch_url_with_aiohttp(url))

# strings = html.xpath(f'//{tag}[contains(., "{found_text})]//text()')

# if text:
#     text = "".join(strings)
#     print(f"{text=}")
# else:
#     print("not found")
# @app.get("/users/{user_id}")
