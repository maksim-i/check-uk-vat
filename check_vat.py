import requests

vat = input()
response = requests.get('https://api.service.hmrc.gov.uk/organisations/vat/'\
                        'check-vat-number/lookup/' + vat)
response_json = response.json()

while True:
    if 'code' in response_json:
        if response_json['code'] == 'INVALID_REQUEST':
            valid = 'false'
            errorMessage = 'Enter the UK VAT number you want to check in the '\
                           'correct format'
            print(valid + '\n' + errorMessage)
    elif 'target' in response_json:
        valid = 'true'
        businessName = response_json['target']['name']
        address = []
        for value in response_json['target']['address'].values():
            address.append(value)
        businessAddress = ' '.join(address)
        print(valid + '\n' + businessName + '\n' + businessAddress)
    break
