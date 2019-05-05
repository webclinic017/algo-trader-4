import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
from datetime import datetime, timedelta
import pendulum


class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode().rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


end = pendulum.now().utcnow()
start = end.subtract(hours=72)
end_str = end.to_iso8601_string()
start_str = start.to_iso8601_string()

api_url = 'https://api.pro.coinbase.com/products/ETH-USD/candles?start=2019-05-02T11:29:42.820602Z&end=2019-05-05T11:29:42.820602Z&granularity=3600')
print(api_url)
auth = CoinbaseExchangeAuth('c7402d99a78b03721e79e66300247286', 'B4HztmlR0n4b1S3M5sVV2wsE1QMp1YFFnG2Ou9AN8cHQMP7sXJirkC8jEt1XtjvUlTSnrS+Xq5Jx2y8EItBIRQ==', 'um4d252jwv')

r = requests.get(api_url, auth=auth)
print(len(r.json()))
