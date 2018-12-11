from coinbase.client import CoinbaseClient
from config import coinbase


class CoinbaseAdapter():

    def __init__(self):
        self.client = CoinbaseClient(coinbase['access_key'],
                                     coinbase['secret_key'],
                                     coinbase['passphrase'],
                                     coinbase['url'])

    def get_accounts(self):
        return self.client.get_accounts()

    def create_order(self):
        # TODO: Make orders dict a param.

        order = {
            'size': 1.0,
            'price': 1.0,
            'side': 'buy',
            'product_id': 'BTC-USD',
        }
        return self.client.create_order(order)
