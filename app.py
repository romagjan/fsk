from flask import Flask
from parser import *
URLs = [
            'https://a101.ru/api/v2/flat/?filter_type=price&limit=50&complex=18',
         
            'https://a101.ru/api/v2/flat/?filter_type=price&limit=2000&complex=17',
            'https://a101.ru/api/v2/flat/?filter_type=price&limit=2000&complex=123',
            'https://a101.ru/api/v2/flat/?filter_type=price&limit=1000&complex=78',
            'https://a101.ru/api/v2/flat/?filter_type=price&limit=200&complex=127',
         
        ]


fsk_objects = [
        'skygarden',
        'sydney-city',
        'arhitektor',
        'rezhiser',
        'rihard',
        'rotterdam',
        'rimskiy',
        'nastroenie',
        'datskij-kvartal',
        'dvizhenie-govorovo',
        'skolkovskiy',
        'skandinavskiy',
        'domdyhanie',
        'zarechnyj',
        'pokolenie',
        ]
dsk_objects = [
        '1-leningradskij',
        'uznaa-bitca'
        ]
URL_FSK='https://fsk.ru/object_id/flats'
URL_DSK='https://www.dsk1.ru/object_id/flat'
app = Flask(__name__)


@app.route('/')
def home():
    result = ''
    for obj in fsk_objects:
        
        result += scrape_site(URL_FSK.replace('object_id',obj))
    
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
