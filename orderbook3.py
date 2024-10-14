import requests

def obtener_orderbook(symbol, scale):
    url = f"https://api.poloniex.com/markets/{symbol}/orderBook"
    params = {"scale": scale, "limit": 15}  # Limitamos a 15 órdenes para cada lado
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener el orderbook: {response.status_code}")
        return None

def mostrar_orderbook(data, tipo, symbol):
    if data and tipo in data:
        print(f"\n{'Compras' if tipo == 'bids' else 'Ventas'} ({symbol}):")
        print("{:<12} {:<15} {:<15}".format(f"Precio({symbol.split('_')[1]})", f"Cantidad({symbol.split('_')[0]})", "Total de compra"))
        print("-" * 42)
        
        acumulado = 0
        for orden in reversed(data[tipo]) if tipo == "asks" else data[tipo]:
            precio, cantidad = float(orden[0]), float(orden[1])
            total = precio * cantidad
            acumulado += total
            print("{:<12.8f} {:<15.2f} {:<15.2f}".format(precio, cantidad, acumulado))
    else:
        print(f"No se pudo obtener el orderbook de {tipo}")

# Valores predefinidos
symbol = "NEIRO_USDT"
scale = "0.00001"

# Obtener y mostrar el orderbook
orderbook = obtener_orderbook(symbol, scale)
if orderbook:
    mostrar_orderbook(orderbook, "bids", symbol)
    mostrar_orderbook(orderbook, "asks", symbol)
