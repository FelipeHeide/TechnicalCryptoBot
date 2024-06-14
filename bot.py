import pandas as pd
import requests
import time
import funciones

cantidad = 0
precio_de_compra = 0
url = 'https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USD&limit=2000&aggregate=1'
response = requests.get(url)
data = response.json()
price_data = data['Data']['Data']
precios_historicos=[]
for price in price_data:
    precios_historicos.append(price['close'])

while True:
    bol = []
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
    eth_price = response.json()['bitcoin']['usd']
    precios_historicos.append(eth_price)

    RSI_75 = funciones.rsi(precios_historicos[len(precios_historicos)-75:-1])
   

    MACD = funciones.macd(precios_historicos[len(precios_historicos)-75:-1])
    MMS = funciones.mms(precios_historicos[len(precios_historicos)-50:-1])
    Nivel_Soporte, Nivel_Resistencia = funciones.Nivel_Soporte_Resistencia(precios_historicos[len(precios_historicos)-50:-1])

    print(f"CURRENT BNB: {eth_price}")
    print("________________________________________________________________________________")
    print(f"RSI 75: {RSI_75}")
    print(f"MACD: {MACD}")
    print(f"MMS: {MMS}")
    print(f"Nivel_Soporte: {Nivel_Soporte}")
    print(f"Nivel_Resistencia: {Nivel_Resistencia}")
    print("\n")
    if RSI_75 < 40:
        RSI_75_ES= "SuperPositivo"
    elif RSI_75 >70:
        RSI_75_ES= "SuperNegativo"
    elif RSI_75-40>70-RSI_75:
        RSI_75_ES = "Negativo"
    elif RSI_75-40<70-RSI_75:
        RSI_75_ES = "Positivo"
    if MACD < 0:
        MACD_ES= "Negativo"
    elif MACD > 0:
        MACD_ES = "Positivo"

    if eth_price-Nivel_Soporte>Nivel_Resistencia-eth_price:
        Nivel_ES = "Positivo"
    elif eth_price-Nivel_Soporte<Nivel_Resistencia-eth_price:
        Nivel_ES = "Negativo"

    if MMS>eth_price:
        MMS_ES = "Negativo"
    elif MMS<eth_price:
        MMS_ES = "Positivo"

    print("RSI: "+RSI_75_ES)
    print("MACD: "+MACD_ES)
    print("MMS: "+MMS_ES)
    print("NIVEL: "+Nivel_ES)
    print("\n")

    if precio_de_compra!=0 and cantidad!=0:
        print("Cantidad Invertida: "+str(cantidad))
        print("Precio De Compra: "+str(precio_de_compra))
        x = eth_price - precio_de_compra
        if x == 0:
            ganancias = 0
            print("Desde la compra hubo un aumento del: " + str(ganancias)+"%")       
            print("Ganaste: " + str(ganancias/100*precio_de_compra))
            print("Ahora tienes: " + str(precio_de_compra+(ganancias/100*precio_de_compra)))
        else:
            y = precio_de_compra / x
            ganancias = 100 /  y
            print("Desde la compra hubo un aumento del: " + str(ganancias)+"%")       
            print("Ganaste: " + str(cantidad/100*ganancias))
            print("Ahora tienes: " + str(cantidad+(cantidad/100*ganancias)))

    if precio_de_compra==0:
        decision = input("Quieres invertir [S]i, [N]o: ")
        if decision.lower() == "s":
            cantidad = float(input("Quantidad: "))
            precio_de_compra = eth_price
        else:
            print("No se invertira")
    print("\n")
    print("\n")
    time.sleep(60)
    


