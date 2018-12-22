from algotrader import logger
from algotrader.exchange.coinbase.adapter import CoinbaseAdapter
from algotrader.storage.manager import StorageManager


# TODO: Get rid of coinbase specific code.
class OrderChecker():

    def __init__(self, storage: StorageManager, exchange):
        self.exchange_dict = {
            'coinbase': CoinbaseAdapter,
        }
        self.exchange = exchange
        self.exchange_adapter = None
        self._get_exchange_adapter()
        self.storage = storage

    # TODO: Should be able to work with more than one exchange.
    def _get_exchange_adapter(self):
        adapter_cls = self.exchange_dict[self.exchange]
        # TODO: Rename
        self.exchange_adapter = adapter_cls()

    def check_orders(self):
        statuses = ['pending', 'open']  # TODO: These should be constant and global.
        orders = self.storage.get_orders(statuses)

        for order in orders:
            # TODO: order_result['id'] already in db, decrease API calls.
            order_result = self.excchange_adapter.get_order(order.id)
            coinbase_fills = self.exchange_adapter.get_fills(order_result['id'])
            persisted_fills = order.get('fills')
            new_fills = self._get_different_fills(coinbase_fills, persisted_fills)

            if not new_fills:
                continue

            logger.info('New Fills: ' + str(new_fills))
            self.storage.update(order.id, new_fills, order.status)  # TODO: order.status or order_result status?

    def _get_new_fills(self, coinbase_fills: list, persisted_fills: list):
        """
        Find all different fill objects by comparing two lists where one is from coinbase and the other one is from db.
        """
        exchange_fills = set(coinbase_fills)
        db_fills = set(persisted_fills)

        return list(exchange_fills.difference(db_fills))
