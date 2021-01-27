import requests, json

base_url = 'https://pro-api.coinmarketcap.com'
api_key = '9c7a3492-2814-4e19-895a-ae25bbbb76d0'

def listing():
        url = f'{base_url}/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY={api_key}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            for registro in data['data']:
                print(registro['symbol'])

        else:
            print("Se ha producido un error", respuesta.status_code)

if __name__ == '__main__':
    listing()

'''
def conversion(from_currency, to_currency, from_quantity):
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '9c7a3492-2814-4e19-895a-ae25bbbb76d0' 
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
'''