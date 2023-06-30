# Google Web Scrapper

Este es un Scrapper de datos desarrollado en Python que permite obtener URLs de resultados de búsqueda de Google. Utiliza bibliotecas como asyncio, aiohttp y BeautifulSoup para realizar solicitudes HTTP asincrónicas a Google y extraer las URLs relevantes de los resultados de búsqueda.

## Requisitos

Para poder ejecutar este Web Scrapper, es necesario tener instaladas las siguientes bibliotecas:

- Python 3
- aiohttp
- BeautifulSoup4
- Huepy (Opcional)

Puedes instalar estas dependencias utilizando pip con el siguiente comando:

```bash
pip install -r requirements.txt
```

## Uso

1. Modifica el parametro de la ultima linea de codigo que contiene la ejecucion de la funcion main, esta es la query a realizar a google

2. Modifica el segundo parametro, si se pasa True guarda los resultados en un archivo de texto y si no se pasa un parametro los imprimira con colores mediante la libreria huepy

## License

[MIT](https://choosealicense.com/licenses/mit/)
