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