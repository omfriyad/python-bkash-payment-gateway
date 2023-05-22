import requests


class bKashCheckoutAPI(object):
    def __init__(self, base_url, username, password, app_key, app_secret):
        self.base_url = f'{base_url}/checkout'
        self.username = username
        self.password = password
        self.app_key = app_key
        self.app_secret = app_secret

    def get_token(self):
        data = {'app_key': self.app_key, 'app_secret': self.app_secret}
        headers = {'Content-Type': 'application/json',
                   'password': self.password,
                   'username': self.username}
        url = self.base_url + '/token/grant'
        response = requests.post(url, json=data, headers=headers)
        return response.json()['id_token']

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            'Authorization': self.get_token(),
            'X-APP-Key': self.app_key
        }

    def create_payment(self, total, callback_url, invoice_id):
        data = {'mode': '0011',
                'amount': total,
                'payerReference': " ",
                'callbackURL': callback_url,
                'currency': 'BDT',
                'intent': 'sale',
                'merchantInvoiceNumber': invoice_id
                }
        url = self.base_url + "/create"

        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def execute(self, payment_id):
        url = self.base_url + '/execute'
        data = {"paymentID": payment_id}

        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def query(self, payment_id):
        url = f'{self.base_url}/payment/query/{payment_id}'
        response = requests.get(url, headers=self.headers)
        return response.json()
