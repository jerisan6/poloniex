import requests
from dotenv import load_dotenv
import os

load_dotenv()

def conectar_poloniex():
    url = "https://api.poloniex.com/markets"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Conexión exitosa con la API de Poloniex")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de Poloniex: {e}")
        return None

resultado = conectar_poloniex()
if resultado:
    print(f"Se recibieron datos de {len(resultado)} mercados")