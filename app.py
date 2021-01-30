import os
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

# создали ендпоинт
@app.route('/webhook2')
def hello_slack():
    # получили данные из запроса
    request_json = request.get_json(silent=True, force=True)
    # тут ваш код возьмет запрос и вернет в ответ любой dict объект ответа, можно даже пустой
    # примерно так request_json -> response_body_json
    ...
    response_body = json.dumps(request_json)
    # упаковали все в корректный респонс
    response = make_response((response_body['challenge']),200)
    response.headers['Content-Type'] = 'text/plain'
    # и вернули
    return response

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
