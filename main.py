import requests, json
from flask import Flask, render_template
from flask import request, redirect

app = Flask('app')

API_KEY = '371a15a5-03d7-425d-a3b6-373a2c1a9f66'

def pl_search(text: str, page: int): 
    url = f'https://search-maps.yandex.ru/v1/?text=Места для Нового года рядом с {text}, Москва&type=biz&lang=ru_RU&results={page * 5}&apikey={API_KEY}'
    response = requests.get(url)
    if not response.ok:
        print("No data")
        return [{'code_error': "Code error: no places found"}]
    json_data = response.json()
    data_p = []
    for data_json in json_data['features']:
        data = {}
        data['coordinates'] = data_json['geometry']['coordinates'] if 'coordinates' in data_json['geometry'].keys() else "Не найдены"
        data['name'] = data_json['properties']['name'] if 'name' in data_json['properties'].keys() else "Не найдено"
        data['site'] = data_json['properties']['CompanyMetaData']['url'] if 'url' in data_json['properties']['CompanyMetaData'].keys() else "Не найден"
        data['id'] = data_json['properties']['CompanyMetaData']['id'] if 'id' in data_json['properties']['CompanyMetaData'].keys() else "Не найден"
        data['address'] = data_json['properties']['CompanyMetaData']['address'] if 'address' in data_json['properties']['CompanyMetaData'].keys() else "Не найден"
        data_p.append(data)
    print(data_p)
    return data_p


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        request_text = request.form.get('search')
        print(request_text)
        return redirect('/results/' + request_text + '/1/')
    
@app.route('/results/<string:request_text>/<int:page>/', methods=['GET'])
def search_results(request_text, page):
    if request.method == 'GET':
        results = pl_search(request_text, page)
        return render_template('search.html', results = results, api_key=API_KEY)
    else:
        return 'Error: use method "GET"'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)