import asyncio
import re
from aiohttp import ClientSession
from bs4 import BeautifulSoup


class GoogleScrapper:
    def __init__(self, query):
        self.query = query
        self.base_url = "https://www.google.com/search?q="
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        }
        self.client = None

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
            if href and self.validate_url(href) and "google" not in href:
                urls.append(href)
        return urls

    async def scrape_url(self, url):
        html = await self.get_html(url)
        # with open("test.html", "w", encoding="utf-8") as f:
        # f.write(html)
        if "CAPTCHA" in html:
            raise Exception("Tu IP requiere realizar una prueba de CAPTCHA")
        return self.get_urls_from_html(html)

    async def scrape_urls(self, limit=10):
        if not isinstance(limit, int) or limit not in range(10, 10000, 10):
            raise ValueError(
                "El límite debe ser un entero entre 10 y 10000 (de 10 en 10)"
            )
        urls = []
        tasks = []
        url = self.base_url + self.query
        tasks.append(self.scrape_url(url))
        for i in range(10, limit, 10):
            url_mod = url + "&start=" + str(i)
            tasks.append(self.scrape_url(url_mod))
        results = await asyncio.gather(*tasks)
        for result in results:
            urls.extend(result)
        return urls

    def close(self):
        if self.client:
            asyncio.create_task(self.client.close())
