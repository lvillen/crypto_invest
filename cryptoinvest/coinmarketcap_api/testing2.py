import requests 

direccion = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=1&symbol=EUR&convert=BTC&CMC_PRO_API_KEY=9c7a3492-2814-4e19-895a-ae25bbbb76d0" #URL a la que quiero llamar

#Hacer petición http
respuesta = requests.get(direccion)

if respuesta.status_code == 200:
    # Esto era una comprobación previa para ver que todo salía bien. 'print(respuesta.text)'
    print(respuesta.text)
    datos = respuesta.json()
    # Para ver que ha creado el fichero, podríamos hacer un print(datos)
    print(datos)
else:
    print("Se ha producido un error", respuesta.status_code)