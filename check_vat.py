import flask
import base64
import os
import requests
import json

app = flask.Flask(__name__)
app.config['DEBUG'] = False

@app.route('/', methods=['GET'])
def index():
    return '<p>Check a UK VAT number</p><form method="POST"><p></p>'\
           '<input name="vat"><span> </span>'\
           '<input type="submit" value="Check"></form>'

@app.route('/get_token', methods=['GET'])
def get_token():
    token = 'Token ' + str(base64.b64encode(os.urandom(24)).decode('utf-8'))
    return token

@app.route('/', methods=['POST'])
def vat_input_redirect():
    vat = flask.request.form['vat']
    response = flask.redirect('/fiscal-number-information/GB/' + vat)
    response.headers['Authorization'] = get_token()
    return response

@app.route('/fiscal-number-information/GB/<vat_input>')
def check_vat(vat_input):
    base_url = 'https://api.service.hmrc.gov.uk'
    lookup_path = '/organisations/vat/check-vat-number/lookup/'
    response = requests.get(base_url + lookup_path + vat_input)
    response.headers['Authorization'] = get_token()
    response_json = response.json()

    result_dict = dict()
    while True:
        if 'code' in response_json:
            if response_json['code'] == 'INVALID_REQUEST':
                result_dict['valid'] = 'false'
                result_dict['errorMessage'] = 'Enter the UK VAT number you '\
                                              'want to check in the '\
                                              'correct format'
            else:
                result_dict['valid'] = 'false'
                result_dict['errorMessage'] = response_json['message']
        elif 'target' in response_json:
            result_dict['valid'] = 'true'
            result_dict['businessName'] = response_json['target']['name']
            address = []
            for value in response_json['target']['address'].values():
                address.append(value)
            businessAddress = ' '.join(address)
            result_dict['businessAddress'] = businessAddress
        break
    return result_dict

app.run()
