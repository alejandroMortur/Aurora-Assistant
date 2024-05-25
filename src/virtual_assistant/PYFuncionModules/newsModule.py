import os
from dotenv import load_dotenv
import requests
from newsapi import NewsApiClient

# Carga las variables de entorno desde el archivo .env
load_dotenv()

def get_country_from_location(location):
    try:
        # URL de la API de Nominatim para buscar la localidad
        url = "https://nominatim.openstreetmap.org/search"

        # Parámetros de búsqueda
        params = {
            "q": location,
            "format": "json",
            "limit": 1
        }

        # Realiza la solicitud GET a la API de Nominatim
        response = requests.get(url, params=params)

        # Si la solicitud es exitosa (código de respuesta 200)
        if response.status_code == 200:
            # Parsea la respuesta JSON para obtener la información de ubicación
            data = response.json()
            if data:
                return data[0]["display_name"].split(",")[-1].strip()
            else:
                print("Location not found:", location)
                return None
        else:
            # Si la solicitud falla, muestra un mensaje de error
            print("---------------------------")
            print("Error retrieving location information:", response.status_code)
            print("---------------------------")
            return None
    except Exception as e:
        print("---------------------------")
        print("An error occurred:", e)
        print("---------------------------")
        return None

def get_top_headlines(api_key, location):
    try:
        # Obtiene el país desde la ubicación
        country = get_country_from_location(location)
        if country:
            # Inicializa el cliente de News API
            newsapi = NewsApiClient(api_key=api_key)
            
            # Obtiene los titulares principales
            top_headlines = newsapi.get_top_headlines(country=country)

            if top_headlines['status'] == 'ok':
                # Imprime los titulares principales
                print("Titulares principales:")
                for article in top_headlines['articles']:
                    print("Título:", article['title'])
                    print("Descripción:", article['description'])
                    print("\n")
            else:
                print("Error retrieving top headlines:", top_headlines['status'])
        else:
            print("Error retrieving country from location")
    except Exception as e:
        print("An error occurred:", e)

# Ejemplo de uso
api_key = os.getenv("APINEWS")
location = "Munich"  # Puedes proporcionar cualquier localidad aquí
get_top_headlines(api_key, location)
