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
            # print(f"Par: {item['symbol']}, Precio: {item['price']}, Cambio diario: {item['dailyChange']}")
    
    print(f"\nNúmero de pares con {moneda_base}: {len(pares_usdt)}")
    print(f"Monto inicial: {monto_inicial} {moneda_base}")
    print(f"Beneficio mínimo buscado: {beneficio_minimo * 100}%")
else:
    print(f"Error al obtener datos: {response.status_code}")

def encontrar_ruta_arbitraje(pares, monto_inicial, beneficio_minimo):
    mejores_rutas = []
    for par1 in pares:
        for par2 in pares:
            if par1 != par2 and par1[1] == par2[0]:
                for par3 in pares:
                    if par3 != par1 and par3 != par2 and par3[0] == par2[1] and par3[1] == par1[0]:
                        # Calcular el beneficio potencial
                        monto1 = monto_inicial / float(par1[2])
                        monto2 = monto1 / float(par2[2])
                        monto_final = monto2 / float(par3[2])
                        beneficio = (monto_final - monto_inicial) / monto_inicial
                        
                        if beneficio > beneficio_minimo:
                            mejores_rutas.append(([par1, par2, par3], beneficio))
    
    return sorted(mejores_rutas, key=lambda x: x[1], reverse=True)

# Procesar los datos proporcionados
pares_disponibles = []
for linea in datos.split('\n'):
    if linea.startswith('Par:'):
        partes = linea.split(', ')
        simbolos = partes[0].split(': ')[1].split('_')
        precio = float(partes[1].split(': ')[1])
        pares_disponibles.append((simbolos[0], simbolos[1], precio))

monto_inicial = 10  # USDT
beneficio_minimo = 0.001  # 0.1% (reducido para encontrar más oportunidades)

rutas_arbitraje = encontrar_ruta_arbitraje(pares_disponibles, monto_inicial, beneficio_minimo)

if rutas_arbitraje:
    print(f"Se encontraron {len(rutas_arbitraje)} rutas de arbitraje:")
    for i, (ruta, beneficio) in enumerate(rutas_arbitraje[:5], 1):  # Mostrar las 5 mejores rutas
        print(f"\nRuta {i}:")
        print(f"{monto_inicial} USDT ->")
        monto = monto_inicial
        for par in ruta:
            m
else:
    print("No se encontró una ruta de arbitraje válida con el beneficio mínimo especificado.")

print(f"\nNúmero de pares analizados: {len(pares_disponibles)}")