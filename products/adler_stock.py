import requests
from decouple import config

def stock_status(nomen):
    r = requests.get(config('ADLER_JSON'))

    data = r.json()

    #input_nomen = str(input('Vlož nomenklaturu: '))

    data_nomen = data['nomen']
    i = next((index for (index, d) in enumerate(data_nomen) if d["number"] == nomen), None)
    index = int(i)


    name = data['nomen'][index]['name'] 
    number = data['nomen'][index]['number'] 
    on_stock = data['nomen'][index]['on_stock']

    #string = str(name) + ' s kódem ' + str(number) + ' je na skladě: ' + str(on_stock) + ' ks.'

    return on_stock
