import requests
from itertools import permutations

MONEDA_BASE = "USDT"
BENEFICIO_MINIMO_PORCENTUAL = 1  # 1%
MONTO_INICIAL = 10  # USDT

def obtener_mercados():
    respuesta = requests.get("https://api.poloniex.com/markets")
    print(f"Código de estado de la respuesta: {respuesta.status_code}")
    datos = respuesta.json()
    print(f"Tipo de datos recibidos: {type(datos)}")
    print(f"Número de elementos recibidos: {len(datos)}")
    
    mercados = {}
    pares_usdt = []
    for m in datos:
        if 'symbol' in m and 'symbolTradeLimit' in m and 'lowestAsk' in m['symbolTradeLimit']:
            precio = m['symbolTradeLimit']['lowestAsk']
            if precio != '0':
                mercados[m['symbol']] = float(precio)
                if MONEDA_BASE in m['symbol']:
                    pares_usdt.append(m['symbol'])
    
    print(f"Se obtuvieron {len(mercados)} pares de trading con precio válido")
    print(f"Pares con {MONEDA_BASE}: {len(pares_usdt)}")
    print(f"Primeros 5 pares con {MONEDA_BASE}: {pares_usdt[:5]}")
    print(f"Primeros 10 pares de trading: {list(mercados.keys())[:10]}")
    return mercados

def calcular_beneficio(ruta, precios):
    try:
        precio_inicial = precios[ruta[0]]
        precio_intermedio = precios[ruta[1]]
        precio_final = precios[ruta[2]]
        return (MONTO_INICIAL / precio_inicial * precio_intermedio / precio_final) - MONTO_INICIAL
    except KeyError as e:
        print(f"Error al calcular beneficio para la ruta {ruta}: {e}")
        return float('-inf')

def encontrar_rutas_rentables(mercados):
    pares_base = [par for par in mercados if MONEDA_BASE in par]
    print(f"Pares con {MONEDA_BASE}: {len(pares_base)}")
    print(f"Todos los pares con {MONEDA_BASE}: {pares_base}")
    
    monedas = set()
    for par in mercados.keys():
        monedas.update(par.split('_'))
    monedas.discard(MONEDA_BASE)
    print(f"Monedas disponibles: {len(monedas)}")
    print(f"Primeras 10 monedas: {list(monedas)[:10]}")
    
    rutas_posibles = [
        (f"{MONEDA_BASE}_{a}", f"{a}_{b}", f"{MONEDA_BASE}_{b}")
        for a, b in permutations(monedas, 2)
        if f"{MONEDA_BASE}_{a}" in mercados and f"{a}_{b}" in mercados and f"{MONEDA_BASE}_{b}" in mercados
    ]
    print(f"Rutas posibles: {len(rutas_posibles)}")
    
    todas_las_rutas = [
        {'ruta': ruta, 'beneficio': calcular_beneficio(ruta, mercados)}
        for ruta in rutas_posibles
    ]
    
    rutas_rentables = [
        ruta for ruta in todas_las_rutas
        if ruta['beneficio'] > MONTO_INICIAL * BENEFICIO_MINIMO_PORCENTUAL / 100
    ]
    
    return todas_las_rutas, rutas_rentables

if __name__ == "__main__":
    try:
        mercados = obtener_mercados()
        todas_las_rutas, rutas_rentables = encontrar_rutas_rentables(mercados)
        
        print(f"Se encontraron {len(rutas_rentables)} rutas rentables:")
        for ruta in rutas_rentables[:5]:
            beneficio_porcentual = (ruta['beneficio'] / MONTO_INICIAL) * 100
            print(f"Ruta: {' -> '.join(ruta['ruta'])}")
            print(f"Beneficio: {ruta['beneficio']:.2f} USDT ({beneficio_porcentual:.2f}%)")
            print("---")
        
        if not rutas_rentables:
            print("No se encontraron rutas rentables. Mostrando algunas rutas no rentables:")
            for ruta in sorted(todas_las_rutas, key=lambda x: x['beneficio'], reverse=True)[:5]:
                beneficio_porcentual = (ruta['beneficio'] / MONTO_INICIAL) * 100
                print(f"Ruta: {' -> '.join(ruta['ruta'])}")
                print(f"Beneficio: {ruta['beneficio']:.6f} USDT ({beneficio_porcentual:.6f}%)")
                print("---")
        
        if not todas_las_rutas:
            print("No se encontraron rutas posibles. Mostrando algunos pares de trading:")
            for par, precio in list(mercados.items())[:10]:
                print(f"Par: {par}, Precio: {precio}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
