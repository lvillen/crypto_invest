import requests, json

direccion = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=1&symbol=BTC&convert=EUR&CMC_PRO_API_KEY=9c7a3492-2814-4e19-895a-ae25bbbb76d0" #URL a la que quiero llamar
respuesta = requests.get(direccion)

if respuesta.status_code == 200:
    datos = respuesta.json()

    with open('datos.txt', 'w') as f:
        json.dump(datos, f)

else:
    print("Se ha producido un error", respuesta.status_code)