import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase


# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        # if request.body:
        #     b = base64.b64encode(request.body).decode()
        # else:
        #     b = ''
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        print('YYY message: ', message)
        print('XXX message: ', type(message))
        print('XXX hmac_key: ', type(hmac_key))
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        # signature_b64 = signature.digest().encode('base64').rstrip('\n')
        signature_b64 = base64.b64encode(signature.digest()).decode().rstrip('\n')
        print('XXX signature: ', signature_b64)

        request.headers.update({

           'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

