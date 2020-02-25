import requests
from decouple import config

def load_stock():
     r = requests.get(config('ADLER_JSON'))
     data = r.json()
     return data

def stock_status(data, nomen):

    data_nomen = data['nomen']
    i = next((index for (index, d) in enumerate(data_nomen) if d["number"] == nomen),)
    index = int(i)

    on_stock = data['nomen'][index]['on_stock']

    return on_stock
