from algotrader import logger
from algotrader.exchange.coinbase.adapter import CoinbaseAdapter


class OrderChecker():

    def __init__(self, storage):
        self.coinbase_adapter = CoinbaseAdapter()
        self.storage = storage

    def check_orders(self):
        statuses = ['pending', 'open']  # These should be constant and global.
        orders = self.storage.get_orders(statuses)

        for order in orders:
            order_result = self.coinbase_adapter.get_order(order.id)
            coinbase_fills = self.coinbase_adapter.get_fills(order_result['id'])
            persisted_fills = order.get('fills')
            new_fills = self._get_different_fills(coinbase_fills, persisted_fills)

            if not new_fills:
                continue

            logger.info('New Fills: ' + str(new_fills))
            self.storage.update(order.id, new_fills, order.status)  # TOOD: order.status or order_result status?

    def _get_different_fills(self, coinbase_fills, persisted_fills=[]):
        """
        Find all different fill objects by comparing two lists where one is from coinbase and the other one is from db.
        """
        diff_fills = []
        for coinbase_fill in coinbase_fills:
            for persisted_fill in persisted_fills:
                if coinbase_fill['trade_id'] == persisted_fill['trade_id']:
                    diff_fills.append(coinbase_fill)
        return diff_fills
