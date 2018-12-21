from decimal import Decimal, ROUND_DOWN

from algotrader.exchange.coinbase.adapter import CoinbaseAdapter
from algotrader.config import coinbase as coinbase_config
from algotrader.database.mongo_helper import Signal, Order
from algotrader.trade_signal import TradeSignal
from algotrader import logger


class OrderManager():

    def __init__(self):
        self.adapter = CoinbaseAdapter()

    def process(self, trade_signal: TradeSignal):
        signal = Signal(signal_id=trade_signal.signal_id,
                        product_id=trade_signal.product_id,
                        order_type=trade_signal.type,
                        side=trade_signal.side,
                        size=trade_signal.size)
        signal.save()
        logger.info('Persisted signal %s ', signal)

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

        persist_order = Order(
            signal_id=trade_signal.order_id,
            order_id=coinbase_order['id'],
            price=coinbase_order.get('price'),
            side=coinbase_order['side'],
            size=coinbase_order['size'],
            product_id=coinbase_order['product_id'],
            created_at=coinbase_order['created_at'],
            done_at=coinbase_order.get('done_at'),
            status=coinbase_order['status'],
            type=coinbase_order['type']
        )
        persist_order.save()

    def get_order(self, order_obj):
        response = self.adapter.get_order(order_obj['order_id'])
        return response

    # TODO: Implement
    def give_decision(self, order_response):
        pass
