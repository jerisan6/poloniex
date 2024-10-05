import requests
import json
from datetime import datetime

def obtener_libro_ordenes(simbolo):
    url = f"https://api.poloniex.com/markets/BTC_USDT/orderBook"
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos = respuesta.json()
        
        asks = datos.get('asks', [])
        bids = datos.get('bids', [])
        
        if asks and bids:
            resultado = {
                "time": int(datetime.now().timestamp() * 1000),
                "scale": "0.01",
                "asks": [],
                "bids": [],
                "ts": int(datetime.now().timestamp() * 1000)
            }
            
            for i in range(0, min(20, len(asks)), 2):
                resultado["asks"].extend([asks[i], asks[i+1]])
            
            for i in range(0, min(20, len(bids)), 2):
                resultado["bids"].extend([bids[i], bids[i+1]])
            
            # Formatear la salida en columnas
            salida = "Ofertas de venta (Asks):\n"
            salida += "Precio (USDT)\tCantidad (BTC)\tTotal (USDT)\n"
            for i in range(0, len(resultado["asks"]), 2):
                precio = float(resultado["asks"][i])
                cantidad = float(resultado["asks"][i+1])
                total = precio * cantidad
                salida += f"{precio}\t{cantidad}\t{total}\n"
            
            salida += "\nOfertas de compra (Bids):\n"
            salida += "Precio (USDT)\tCantidad (BTC)\tTotal (USDT)\n"
            for i in range(0, len(resultado["bids"]), 2):
                precio = float(resultado["bids"][i])
                cantidad = float(resultado["bids"][i+1])
                total = precio * cantidad
                salida += f"{precio}\t{cantidad}\t{total}\n"
            
            return salida
        else:
            return f"No se pudo obtener el libro de órdenes para {simbolo}"
    
    except requests.RequestException as e:
        return f"Error al hacer la solicitud: {e}"

# Uso de la función
if __name__ == "__main__":
    simbolo = "BTC_USDT"
    resultado = obtener_libro_ordenes(simbolo)
    print(resultado)
