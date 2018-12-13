import json
import boto3
from coinbase.client import CoinbaseClient
from config import aws as aws_config

s3_client = boto3.resource('s3')

bucket_name = aws_config['dev']['s3']['bucket']
object_key = aws_config['dev']['s3']['key']

coinbase_config_s3_object = s3_client.Object(bucket_name, object_key)
coinbase_config = json.loads(coinbase_config_s3_object.get()['Body'].read().decode('utf-8'))


class CoinbaseAdapter():

    def __init__(self):
        self.client = CoinbaseClient(coinbase_config['accessKey'],
                                     coinbase_config['secretKey'],
                                     coinbase_config['passphrase'],
                                     aws_config['dev']['coinbase']['base-endpoint'])

    def get_accounts(self):
        response = self.client.get_accounts()
        return response.json()

    def get_account(self, account_id):
        """
        Example account response;
        {
            'id': 'e6a8d351-027e-487f-94e7-985a9a075090',
            'currency': 'USD',
            'balance': '1735.7693716566837000',
            'available': '1734.7663716566837',
            'hold': '1.0030000000000000',
            'profile_id': 'a6c82597-f923-4e68-a255-21ce5791c8ea'
         }
        """
        response = self.client.get_account(account_id)
        return response.json()

    def get_order(self, order_id):
        response = self.client.get_order(order_id)
        return response.json()

    def submit_order(self, order):
        """
        Example order response;
        {'created_at': '2018-12-11T12:12:30.607493Z',
        'executed_value': '0.0000000000000000',
        'fill_fees': '0.0000000000000000',
        'filled_size': '0.00000000',
        'funds': '1729.5776387400000000',
        'id': 'eea70b05-7bff-4f5c-9f90-49dbfe497555',
        'post_only': False,
        'product_id': 'ETH-USD',
        'settled': False,
        'side': 'buy',
        'size': '1735.76937165',
        'status': 'pending',
        'stp': 'dc',
        'type': 'market'}
        """
        response = self.client.submit_order(order)
        return response.json()
