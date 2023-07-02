import asyncio
from sys import exit as ex
from scrapper import WebScrapper, SearchEngines
from huepy import yellow, red


async def main():
    print("""Motores de busqueda disponibles:
1. GOOGLE
2. ASK""")
    search_engine_input = input("Ingrese el motor de busqueda: ")
    if search_engine_input == "1":
        search_engine = SearchEngines.GOOGLE
    elif search_engine_input == "2":
        search_engine = SearchEngines.ASK
    else:
        print(red("El motor de busqueda ingresado no es valido"))
        ex()

    query = input("Ingrese la consulta: ")
    scrapper = WebScrapper(query, search_engine=search_engine)
    try:
        limit = int(input("Ingrese el limite: "))
        urls = await scrapper.scrape_urls(limit)
        scrapper.close()
    except Exception as e:
        print(e)
        scrapper.close()
        return
    
    input_file = input("Desea generar un archivo con las URLs? (y/n): ")
    if input_file.upper() == "Y":
        name_file = input("Ingrese el nombre del archivo: ")
        with open(name_file, "a", encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")
        print(yellow("URLs guardas exitosamente en el archivo!"))
    else:
        for index, url in enumerate(urls):
            print(yellow(f"[{index + 1}]"), red(url))


if __name__ == "__main__":
    asyncio.run(main())
