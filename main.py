import asyncio
from scrapper import GoogleScrapper
from huepy import yellow, red  # Si no necesitas imprimir comenta esta linea


async def main(query, gen_file=False):
    scraper = GoogleScrapper(str(query))
    try:
        print(
            "Ingrese el limite, debe ser mayor a 10 y ir en 10 en 10, maximo valor 10000\nA continuacion ingrese el limite y luego ENTER"
        )
        urls = await scraper.scrape_urls(int(input()))
        scraper.close()
    except Exception as e:
        print(e)
        scraper.close()
        return

    if gen_file:
        with open("urls.txt", "a", encoding="utf-8") as f:
            for index, url in enumerate(urls):
                f.write(str(f"[{index + 1}]- " + url + "\n"))
    else:
        for index, url in enumerate(urls):
            print(yellow(f"[{index + 1}]"), red(url))


asyncio.run(main("Ropa", True))
