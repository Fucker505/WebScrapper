import asyncio
from scrapper import WebScrapper, SearchEngines
from huepy import blue, red, purple, lgreen


async def main():
    print(
        lgreen(
            """Motores de busqueda disponibles:
1. GOOGLE
2. ASK
3. BING
4. YAHOO

ELIGE EL NUMERO DEL MOTOR!
"""
        )
    )
    search_engine_input = input(blue("Ingrese el motor de busqueda: "))
    if search_engine_input == "1":
        search_engine = SearchEngines.GOOGLE
        print("Motor de busqueda elegido: GOOGLE")
    elif search_engine_input == "2":
        search_engine = SearchEngines.ASK
    elif search_engine_input == "3":
        search_engine = SearchEngines.BING
    elif search_engine_input == "4":
        search_engine = SearchEngines.YAHOO

    else:
        print(red("El motor de busqueda ingresado no esta en nuestra lista de motores"))
        return
    print(purple("El motor de busqueda elegido es: " + search_engine.name + "\n"))

    query = input(blue("Ingrese la consulta: "))
    remove = input(blue("Desea remover las URLs innecesarias? (y/n): ")).upper()
    removeb = True if remove == "Y" else False
    scrapper = WebScrapper(query, search_engine=search_engine, remove_trash=removeb)
    try:
        limit = int(input(blue("Ingrese el limite: ")))
        urls = await scrapper.scrape_urls(limit)
        scrapper.close()
    except Exception as e:
        print(e)
        scrapper.close()
        return

    input_file = input(blue("Desea generar un archivo con las URLs? (y/n): "))
    if input_file.upper() == "Y":
        name_file = input(blue("Ingrese el nombre del archivo: "))
        open(name_file, "w").close()
        with open(name_file, "a", encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")
        print(red("URLs guardas exitosamente en el archivo!"))
    else:
        for index, url in enumerate(urls):
            print(purple(f"[{index + 1}]"), red(url))


if __name__ == "__main__":
    asyncio.run(main())
