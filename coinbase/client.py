import json
import hmac
import hashlib
import time
import base64
import requests


class CoinbaseClient():
    def __init__(self, api_key, secret_key, passphrase, url):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.url = url

    def create_order(self, order):
        path = '/orders'
        return self._make_request('POST', path, data=order)

    def get_accounts(self):
        path = '/accounts'
        return self._make_request('GET', path)

    def _make_request(self, method, path, data=None):
        timestamp = str(time.time())
        message = timestamp + method + path
        if data:
            message = message + json.dumps(data)

        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode().rstrip('\n')

        headers = {
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        url = self.url + path
        # TODO: Handle error cases
        return requests.request(method, url, json=data, headers=headers)
