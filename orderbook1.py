import requests
from datetime import datetime

def obtener_libro_ordenes(symbol="NEIRO_USDT"):
    url = f"https://api.poloniex.com/markets/{symbol}/orderBook"
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos = respuesta.json()
        
        asks = datos.get('asks', [])
        bids = datos.get('bids', [])
        
        if asks and bids:
            resultado = {
                "time": int(datetime.now().timestamp() * 1000),
                "asks": asks[:20],
                "bids": bids[:20],
                "ts": int(datetime.now().timestamp() * 1000)
            }
            
            # Formatear la salida en columnas
            salida = f"Libro de órdenes para {symbol}:\n\n"
            salida += "Ofertas de venta (Asks):\n"
            salida += f"{'Precio (USDT)':<14}{'Cantidad':<18}{'Total (USDT)':<15}\n"
            salida += "-" * 47 + "\n"
            for precio, cantidad in resultado["asks"]:
                precio = float(precio)
                cantidad = float(cantidad)
                total = precio * cantidad
                salida += f"{precio:<14.3f}{cantidad:<18.8f}{total:<15.2f}\n"
            
            salida += "\nOfertas de compra (Bids):\n"
            salida += f"{'Precio (USDT)':<14}{'Cantidad':<18}{'Total (USDT)':<15}\n"
            salida += "-" * 47 + "\n"
            for precio, cantidad in resultado["bids"]:
                precio = float(precio)
                cantidad = float(cantidad)
                total = precio * cantidad
                salida += f"{precio:<14.3f}{cantidad:<18.8f}{total:<15.2f}\n"
            
            return salida
        else:
            return "No se encontraron datos de órdenes."
    except requests.exceptions.RequestException as e:
        return f"Error al obtener el libro de órdenes: {e}"

# Llamada a la función y impresión del resultado
print(obtener_libro_ordenes())
