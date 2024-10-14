import requests

# Variables predefinidas
symbol = "NEIRO_USDT"
scale = "0.01"

def obtener_orderbook(symbol, scale):
    url = f"https://api.poloniex.com/markets/{symbol}/orderBook"
    params = {"scale": scale}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error al obtener el orderbook: {response.status_code}")
        return None

def mostrar_orderbook(data, tipo):
    if data and tipo in data:
        print(f"\nOrderbook de {tipo.capitalize()}:")
        print("{:<15} {:<15} {:<15}".format("Precio", "Cantidad", "Total"))
        print("-" * 45)
        
        for i in range(0, len(data[tipo]), 2):
            precio = data[tipo][i]
            cantidad = data[tipo][i+1] if i+1 < len(data[tipo]) else "N/A"
            
            # Intentamos convertir precio y cantidad a float para el cálculo del total
            try:
                precio_float = float(precio)
                cantidad_float = float(cantidad)
                total = precio_float * cantidad_float
            except ValueError:
                total = "N/A"
            
            print("{:<15} {:<15} {:<15}".format(precio, cantidad, total))
    else:
        print(f"No se pudo obtener el orderbook de {tipo}")

# Obtener y mostrar el orderbook
orderbook = obtener_orderbook(symbol, scale)
if orderbook:
    mostrar_orderbook(orderbook, "bids")
    mostrar_orderbook(orderbook, "asks")
else:
    print(f"No se pudo obtener el orderbook para {symbol}")
