import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_news_today(api_key, query, language,page_size):
    
    sort_by = 'popularity'
    from_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')  # Get news from the last week
    to_date = datetime.today().strftime('%Y-%m-%d')  # Until now
    
    try:
        # Build the URL for the NewsAPI API request
        url = ('https://newsapi.org/v2/everything?'
               f'q={query}&'
               f'from={from_date}&'
               f'to={to_date}&'
               f'sortBy={sort_by}&'
               f'pageSize={page_size}&'
               f'language={language}&'  
               f'apiKey={api_key}')
        
        # Make the GET request to the NewsAPI API
        response = requests.get(url)
        
        # Initialize a list to store the news
        news_list = []
        
        # Check if the request was successful (response code 200)
        if response.status_code == 200:
            # Get the JSON of the response
            data = response.json()
            
            # Check if the answer is "ok"
            if data['status'] == 'ok':
                total_results = data.get('totalResults', 0)
                if total_results > 0:
                    # Iterate over each article and add it to the news list
                    for article in data['articles']:
                        news_list.append({
                            "Título": article['title'],
                            "Descripción": article.get('description', 'Descripción no disponible'),
                            "Contenido": article.get('content', 'Contenido no disponible'),
                            "URL": article['url'],
                            "Fuente": article['source']['name'],
                            "Fecha de publicación": article['publishedAt']
                        })
                else:
                    print("No se encontraron titulares.")
            else:
                print("Error en la respuesta de la API:", data.get('message', 'No se proporcionó mensaje de error.'))
        else:
            print("Error al realizar la solicitud:", response.status_code)
        
        return news_list
        
    except Exception as e:
        print("Ocurrió un error:", e)
        return []

