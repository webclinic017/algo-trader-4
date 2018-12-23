from decimal import Decimal, ROUND_DOWN

from algotrader.exchange.coinbase.adapter import CoinbaseAdapter
from algotrader.signal import TradeSignal, TradeOrder
from algotrader.storage.manager import StorageManager
from algotrader import logger


class OrderManager():
    exchange_types = {
        'coinbase': CoinbaseAdapter,
    }

    STATUS_PENDING = 'pending'
    STATUS_OPEN = 'open'

    def __init__(self, storage: StorageManager, exchange):
        self._exchange = exchange
        self.storage = storage
        self._get_exchange()

    def _get_exchange(self):
        adapter_cls = self.exchange_types[self._exchange]
        self.exchange = adapter_cls()

    def process(self, trade_signal: TradeSignal):
        self.storage.create_signal(trade_signal)

        account = self.exchange.get_account(trade_signal.currency)

        # TODO: Can process only size='all'
        # get maximum amount of balance with scale of 8 digits and rounding down it.
        order_size = Decimal(account['balance']).quantize(Decimal('.0001'), rounding=ROUND_DOWN)

        order = {
            'size': str(order_size),
            'type': trade_signal.order_type,
            'side': trade_signal.side,
            'product_id': trade_signal.product_id,
        }
        logger.info('Submitting order: %s', order)

        submitted_order = self.exchange.submit_order(order)
        if submitted_order is None:
            logger.error('Submitted order is None!')
            return

        logger.info('Received order: %s', submitted_order)

        # TODO: Are all timestamps UTC?
        trade_order = TradeOrder(
            trade_signal.order_id,
            submitted_order['id'],  # TODO: Coinbase specific. Make this more generic.
            submitted_order.get('price'),
            submitted_order['side'],
            submitted_order['size'],
            submitted_order['product_id'],
            submitted_order['created_at'],
            submitted_order.get('done_at'),
            submitted_order['status'],
            submitted_order['type']
        )
        self.storage.create_order(trade_order)

    def get_order(self, order_obj):
        response = self.adapter.get_order(order_obj['order_id'])
        return response

    def check_orders(self):
        statuses = [self.STATUS_PENDING, self.STATUS_OPEN]
        orders = self.storage.get_orders(statuses)

        for order in orders:
            # TODO: order_result['id'] already in db, decrease API calls.
            order_result = self.exchange.get_order(order.id)
            exchange_fills = self.exchange.get_fills(order_result['id'])
            persisted_fills = order.get('fills')
            new_fills = self._get_different_fills(exchange_fills, persisted_fills)

            if not new_fills:
                continue

            logger.info('New Fills: %s', new_fills)
            self.storage.update(order.id, new_fills, order.status)  # TODO: order.status or order_result status?

    def _get_new_fills(self, exchange_fills: list, persisted_fills: list):
        """
        Find all different fill objects by comparing two lists where one is from exchange and the other one is from db.
        """
        exchange_fills = set([fill['trade_id'] for fill in exchange_fills])
        db_fills = set([fill['trade_id'] for fill in persisted_fills])
        diff = list(exchange_fills.difference(db_fills))

        return [fill for fill in exchange_fills if fill['id'] in diff]
