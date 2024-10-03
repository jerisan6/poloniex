import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener las credenciales
api_key = os.getenv('POLONIEX_API_KEY')
api_secret = os.getenv('POLONIEX_SECRET_KEY')

# Mostrar que hay una conexión establecida y las credenciales
print("Conexión establecida con Poloniex API")
print(f"API Key: {api_key}")
print(f"API Secret: {api_secret}")

# Conectarse a la URL y obtener la información
url = 'https://api.poloniex.com/markets/price'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("\nInformación de precios de mercado:")
    for item in data:
        print(f"Símbolo: {item['symbol']}, Precio: {item['price']}, Cambio diario: {item['dailyChange']}")
else:
    print(f"Error al obtener datos: {response.status_code}")