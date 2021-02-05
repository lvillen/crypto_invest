import requests, json, os
from cryptoinvest import application

base_url = 'https://pro-api.coinmarketcap.com'
#api_key = os.environ['API_KEY']
api_key = application.config['API_KEY'] #No puedo lanzar el config sin estar lanzado el Flask run

def listing():
    url = f'{base_url}/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        for registro in data['data']:
            print(registro['symbol'])

    else:
        print('Se ha producido un error', respuesta.status_code)

def conversion(from_quantity, from_currency, to_currency):
    url = f'{base_url}/v1/tools/price-conversion?amount={from_quantity}&symbol={from_currency}&convert={to_currency}&CMC_PRO_API_KEY={api_key}'
    
    print(url)
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return float(data['data']['quote'][to_currency]['price'])
    else:
        print("La API ha fallado con un error", response.status_code)
    
    #Controlar errores 400 / 401 / etc.
            

if __name__ == '__main__':
    conversion(1000, 'BTC', 'ETH')