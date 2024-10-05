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
                "time": datos.get('time', 0),
                "scale": datos.get('scale', '0.00001'),
                "asks": asks[:10],  # Limitamos a 10 entradas para mayor claridad
                "bids": bids[:10],
                "ts": datos.get('ts', 0)
            }
            
            # Formatear la salida en columnas
            salida = f"Libro de órdenes para {symbol}:\n"
            salida += f"Escala: {resultado['scale']}\n\n"
            salida += "Ofertas de venta (Asks):\n"
            salida += f"{'Precio (USDT)':<14}{'Cantidad':<18}{'Total (USDT)':<15}\n"
            salida += "-" * 47 + "\n"
            for i in range(0, len(resultado["asks"]), 2):
                precio = float(resultado["asks"][i])
                cantidad = float(resultado["asks"][i+1].replace('.', ''))
                total = precio * cantidad
                salida += f"{precio:<14.5f}{cantidad:<18.8f}{total:<15.8f}\n"
            
            salida += "\nOfertas de compra (Bids):\n"
            salida += f"{'Precio (USDT)':<14}{'Cantidad':<18}{'Total (USDT)':<15}\n"
            salida += "-" * 47 + "\n"
            for i in range(0, len(resultado["bids"]), 2):
                precio = float(resultado["bids"][i])
                cantidad = float(resultado["bids"][i+1].replace('.', ''))
                total = precio * cantidad
                salida += f"{precio:<14.5f}{cantidad:<18.8f}{total:<15.8f}\n"
            
            return salida
        else:
            return "No se encontraron datos de órdenes."
    except requests.exceptions.RequestException as e:
        return f"Error al obtener el libro de órdenes: {e}"

# Llamada a la función y impresión del resultado
print(obtener_libro_ordenes())