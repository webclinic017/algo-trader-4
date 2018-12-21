from decimal import Decimal, ROUND_DOWN

from algotrader.exchange.coinbase.adapter import CoinbaseAdapter
from algotrader.config import coinbase as coinbase_config
from algotrader.signal import TradeSignal, TradeOrder
from algotrader import storage
from algotrader import logger


class OrderManager():

    def __init__(self, storage):
        self.adapter = CoinbaseAdapter()
        self.storage = storage

    def process(self, trade_signal: TradeSignal):
        storage.create_signal(trade_signal)

        # TODO: Get rid of exchange-specific logic.
        account = self.adapter.get_account(coinbase_config['accounts'][trade_signal.currency])

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

        coinbase_order = self.adapter.submit_order(order)
        if coinbase_order is None:
            logger.error('Coinbase_order is None')
            return

        logger.info('Received order: %s', coinbase_order)

        # TODO: Are all timestamps UTC?
        trade_order = TradeOrder(
            trade_signal.order_id,
            coinbase_order['id'],  # TODO: Coinbase specific. Make this more generic.
            coinbase_order.get('price'),
            coinbase_order['side'],
            coinbase_order['size'],
            coinbase_order['product_id'],
            coinbase_order['created_at'],
            coinbase_order.get('done_at'),
            coinbase_order['status'],
            coinbase_order['type']
        )
        storage.create_order(trade_order)

    def get_order(self, order_obj):
        response = self.adapter.get_order(order_obj['order_id'])
        return response

    # TODO: Implement
    def give_decision(self, order_response):
        pass
