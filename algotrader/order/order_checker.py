from pymongo import MongoClient
from algotrader import logger
from algotrader.exchange.coinbase.adapter import CoinbaseAdapter


class OrderChecker():

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['algotrader']
        self.orders = self.db['orders']
        self.coinbase_adapter = CoinbaseAdapter()

    def check_orders(self):
        for current_order in self.orders.find({'$or': [{'status': 'pending'}, {'status': 'open'}]}):
            order_result = self.coinbase_adapter.get_order(current_order['order_id'])
            logger.info('Order: ' + str(order_result))
            coinbase_fills = self.coinbase_adapter.get_fills(order_result['id'])
            persisted_fills = current_order.get('fills')
            new_fills = self._get_different_fills(coinbase_fills, persisted_fills)
            if not new_fills:
                continue
            logger.info('New Fills: ' + str(new_fills))
            self.orders.update(
                {'order_id': current_order['order_id']},
                {'$push': {'fills': {'$each': new_fills}}, '$set': {'status': order_result['status']}}
            )

    def _get_different_fills(self, coinbase_fills, persisted_fills=[]):
        """
        Find all different fill objects by comparing two lists where one is from coinbase and the other one is from db.
        """
        diff_fills = []
        for coinbase_fill in coinbase_fills:
            for persisted_fill in persisted_fills:
                if self._compare_fills(coinbase_fill, persisted_fill):
                    diff_fills.append(coinbase_fill)
        return diff_fills

    def _compare_fills(self, coinbase_fill, persisted_fill):
        return coinbase_fill['trade_id'] == persisted_fill['trade_id']
