import requests
from typing import List, Dict

def get_usdt_markets() -> List[Dict]:
    url = "https://api.poloniex.com/markets"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Esto lanzará una excepción para códigos de estado HTTP no exitosos
        
        markets = response.json()
        
        # Filtramos solo los pares que contienen USDT
        usdt_markets = [market for market in markets if market['quoteCurrencyName'] == 'USDT']
        
        return usdt_markets
    except requests.RequestException as e:
        print(f"Error al conectar con la API de Poloniex: {e}")
        return []

# Ejemplo de uso:
if __name__ == "__main__":
    usdt_markets = get_usdt_markets()
    for market in usdt_markets:
        print(f"{market['symbol']}: {market['baseCurrencyName']}/{market['quoteCurrencyName']}")