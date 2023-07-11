import asyncio
import re
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from enum import Enum
from urllib.parse import unquote


class SearchEngines(Enum):
    GOOGLE = "https://www.google.com/search?q="
    ASK = "https://www.ask.com/web?q="
    BING = "https://www.bing.com/search?q="
    YAHOO = "https://search.yahoo.com/search?p="


class WebScrapper:
    def __init__(self, query, search_engine=SearchEngines.GOOGLE, remove_trash=True):
        self.query = query
        self.search_engine = search_engine
        self.base_url = search_engine.value
        if search_engine == SearchEngines.GOOGLE:
            self.page = "&start="
        elif search_engine == SearchEngines.ASK:
            self.page = "&page="
        elif search_engine == SearchEngines.BING:
            self.page = "&first="
        elif search_engine == SearchEngines.YAHOO:
            self.page = "&b="

        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        }
        self.client = None
        self.remove_trash = remove_trash

    @staticmethod
    def validate_url(url):
        regex = re.compile(
            r"^(?:http|ftp)s?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        return re.match(regex, str(url)) is not None

    async def get_html(self, url):
        if self.client is None:
            self.client = ClientSession(headers=self.headers)
        async with self.client.get(url) as response:
            return await response.text()

    def get_urls_from_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        urls = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and self.validate_url(href):
                if self.remove_trash:
                    if (
                        "microsoft" in href
                        or "bing" in href
                        or "google" in href
                        or "ask" in href
                        or "support" in href
                    ):
                        continue
                if self.search_engine == SearchEngines.YAHOO:
                    try:
                        ru = href.split("RU=")[1].split("RK=")[0]
                        href = unquote(ru)
                        if "yahoo" in href:
                            continue
                        if href.endswith("//"):
                            href = href[0 : href.rfind("//")]
                    except:
                        continue
                urls.append(href)
        return urls

    async def scrape_url(self, url):
        html = await self.get_html(url)
        if "CAPTCHA" in html:
            raise Exception("Tu IP requiere realizar una prueba de CAPTCHA")
        return self.get_urls_from_html(html)

    async def scrape_urls(self, limit=10):
        if not isinstance(limit, int):
            raise TypeError("El limite debe ser un entero")
        if self.search_engine == SearchEngines.GOOGLE and limit not in range(
            10, 10000, 10
        ):
            raise ValueError(
                "El límite debe ser un entero entre 10 y 10000 (de 10 en 10)"
            )
        elif (
            self.search_engine == SearchEngines.ASK
        ):
            if limit <= 0 or limit > 100:
                raise ValueError("El límite debe estar en el rango de 1 y 100")
        urls = []
        tasks = []
        url = self.base_url + self.query
        step = 10 if self.search_engine == SearchEngines.GOOGLE else 1
        tasks.append(self.scrape_url(url))
        for i in range(step, limit, step):
            if self.search_engine == SearchEngines.BING:
                i *= 2
            url_mod = url + self.page + str(i)
            tasks.append(self.scrape_url(url_mod))
        results = await asyncio.gather(*tasks)
        for result in results:
            urls.extend(result)
        return list(set(urls))

    def close(self):
        if self.client:
            asyncio.create_task(self.client.close())
            self.client = None
