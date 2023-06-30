# Google Web Scrapper

Este es un Scrapper de datos desarrollado en Python que permite obtener URLs de resultados de búsqueda de Google. Utiliza bibliotecas como asyncio, aiohttp y BeautifulSoup para realizar solicitudes HTTP asincrónicas a Google y extraer las URLs relevantes de los resultados de búsqueda.

## Requisitos
- Python 3

Para poder ejecutar este Web Scrapper, es necesario tener instaladas las siguientes bibliotecas:
- aiohttp
- BeautifulSoup4
- Huepy (Opcional)


## Uso

1. Modifica el parametro de la ultima linea de codigo que contiene la ejecucion de la funcion main, esta es la query a realizar a google

2. Modifica el segundo parametro, si se pasa True guarda los resultados en un archivo de texto y si no se pasa un parametro los imprimira con colores mediante la libreria huepy

Para poder ejecutarlo ejecuta las siguientes ordenes en tu shell
```bash
git clone https://github.com/Fucker505/WebScrapper.git
cd WebScrapper
pip install -r requirements.txt
python main.py
```

## License

[MIT](https://choosealicense.com/licenses/mit/)