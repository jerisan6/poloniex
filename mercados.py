import os, requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener las credenciales
api_key, api_secret = os.getenv('POLONIEX_API_KEY'), os.getenv('POLONIEX_SECRET_KEY')

# Mostrar que hay una conexión establecida y las credenciales
print(f"Conexión establecida con Poloniex API\nAPI Key: {api_key}\nAPI Secret: {api_secret}")

# Conectarse a la URL y obtener la información
response = requests.get('https://api.poloniex.com/markets')

if response.status_code == 200:
    print("\nInformación de precios de mercado:")
    [print(f"Símbolo: {item['symbol']}, Precio: {item['price']}, Cambio diario: {item['dailyChange']}") for item in response.json()]
else:
    print(f"Error al obtener datos: {response.status_code}")