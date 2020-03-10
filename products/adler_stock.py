import requests
from decouple import config

def load_stock():
     try:
          r = requests.get(config('ADLER_JSON'))
          data = r.json()
          return data
     except json.decoder.JSONDecodeError:
          pass


def stock_status(data, nomen):
     try:
          data_nomen = data['nomen']
          i = next((index for (index, d) in enumerate(data_nomen) if d["number"] == nomen),)
          index = int(i)

          on_stock = data['nomen'][index]['on_stock']
          return on_stock
     except KeyError:
          pass
