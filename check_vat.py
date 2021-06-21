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
    return 'Token ' + str(base64.b64encode(os.urandom(24)).decode('utf-8'))

@app.route('/', methods=['POST'])
def vat_input_redirect():
    vat = flask.request.form['vat']
    return flask.redirect('/fiscal-number-information/GB/' + vat)

@app.route('/fiscal-number-information/GB/')
def empty_field_redirect():
    return flask.redirect('/')

@app.route('/fiscal-number-information/GB/<vat_input>')
def check_vat(vat_input):
    base_url = 'https://api.service.hmrc.gov.uk'
    lookup_path = '/organisations/vat/check-vat-number/lookup/'
    response = requests.get(base_url + lookup_path + vat_input)
    response.headers['Authorization'] = get_token()
    response_json = response.json()

    result_dict = dict()
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

    if 'Authorization' in response.headers:
        print(response.headers['Authorization'])
        return result_dict
    else:
        return '<p>(!) Generate a token at "/get_token" to gain access</p>'

app.run()
