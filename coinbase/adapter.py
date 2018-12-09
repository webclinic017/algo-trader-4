import requests
from pprint import pprint
import json

from coinbase_pro.client import CoinbaseExchangeAuth


class CoinbaseAdapter():

    def __init__(self):
        pass

    def create_order(self):
        passphrase = 'bf4zovy42ca'
        secret_key = 'K+0gUKEBKTZ0SWIqq3PxVjCjvf+HTPAnnffW/aCDtlbYxKDBKM2Mec8Apfr3oxrV4x6urdvoXye5oBJuC/6XOA=='
        access_key = '309832aa37a7698c9e1e63fd4322a094'

        api_url = 'https://api-public.sandbox.pro.coinbase.com'
        auth = CoinbaseExchangeAuth(access_key, secret_key, passphrase)

        # Get accounts
        r = requests.get(api_url + '/accounts', auth=auth)
        pprint(r.json())
        # [{"id": "a1b2c3d4", "balance":...

        # Place an order
        order = {
            'size': 1.0,
            'price': 1.0,
            'side': 'buy',
            'product_id': 'BTC-USD',
        }
        r = requests.post(api_url + '/orders', data=json.dumps(order), auth=auth)
        pprint(r.json())