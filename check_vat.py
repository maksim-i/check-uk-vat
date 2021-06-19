import flask
import requests
import json

app = flask.Flask(__name__)
app.config['DEBUG'] = False

@app.route('/', methods=['GET'])
def home():
    return '<p>Check a UK VAT number</p>'\
           '<form method="POST">'\
           '<input name="vat"><span> </span>'\
           '<input type="submit" value="Check">'\
           '</form>'

@app.route('/', methods=['POST'])
def check_vat():
    vat = flask.request.form['vat']
    base_url = 'https://api.service.hmrc.gov.uk'
    lookup_path = '/organisations/vat/check-vat-number/lookup/'
    response = requests.get(base_url + lookup_path + vat)
    response_json = response.json()

    result_dict = dict()
    while True:
        if 'code' in response_json:
            if response_json['code'] == 'INVALID_REQUEST':
                result_dict['valid'] = 'false'
                result_dict['errorMessage'] = 'Enter the UK VAT number you want '\
                                              'to check in the correct format'
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
