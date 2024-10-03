import os, requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener las credenciales
api_key, api_secret = os.getenv('POLONIEX_API_KEY'), os.getenv('POLONIEX_SECRET_KEY')

# Mostrar que hay una conexión establecida y las credenciales
print(f"Conexión establecida con Poloniex API\nAPI Key: {api_key}\nAPI Secret: {api_secret}")

# Definir variables de trading
moneda_base = "USDT"
beneficio_minimo = 0.01  # 1%
monto_inicial = 10  # USDT

# Conectarse a la URL y obtener la información
response = requests.get('https://api.poloniex.com/markets/price')

if response.status_code == 200:
    print("\nInformación de pares con USDT:")
    pares_usdt = []
    for item in response.json():
        # Filtrar solo los pares que contienen USDT
        if moneda_base in item['symbol']:
            pares_usdt.append(item)
            print(f"Par: {item['symbol']}, Precio: {item['price']}, Cambio diario: {item['dailyChange']}")
    
    print(f"\nNúmero de pares con {moneda_base}: {len(pares_usdt)}")
    print(f"Monto inicial: {monto_inicial} {moneda_base}")
    print(f"Beneficio mínimo buscado: {beneficio_minimo * 100}%")
else:
    print(f"Error al obtener datos: {response.status_code}")