from decimal import Decimal, ROUND_DOWN

from algotrader.exchange.coinbase.adapter import CoinbaseAdapter
from algotrader.config import aws as aws_config
from algotrader.utils.common_utils import CommonUtils
from algotrader.database.mongo_helper import Signal, Order
from algotrader import logger


class OrderManager():

    def __init__(self):
        self.adapter = CoinbaseAdapter()

    def process(self, trade_signal):
        """
            Process the given signal.
            Ex signal;
            {
                "order_id": "ETH-USD_coinbase_1543359420",
                "product_id": "ETH-USD",
                "type": "market",
                "side": "sell",
                "size": "all"
            }
        """
        signal = Signal(signal_id=trade_signal['order_id'],
                        product_id=trade_signal['product_id'],
                        order_type=trade_signal['type'],
                        side=trade_signal['side'],
                        size=trade_signal['size'])
        signal.save()
        logger.info('Persisted signal %s ', signal)
        if trade_signal['side'] == 'buy':
            quote_currency = CommonUtils.get_quote_currency(trade_signal['product_id'])
            account = self.adapter.get_account(aws_config['dev']['coinbase']['accounts'][quote_currency])
        else:
            base_currency = CommonUtils.get_base_currency(trade_signal['product_id'])
            account = self.adapter.get_account(aws_config['dev']['coinbase']['accounts'][base_currency])

        if trade_signal['size'] == 'all':
            # get maximum amount of balance with scale of 8 digits and rounding down it.
            size = Decimal(account['balance']).quantize(Decimal('.0001'), rounding=ROUND_DOWN)
        order = {
            'size': str(size),
            'type': trade_signal['type'],
            'side': trade_signal['side'],
            'product_id': trade_signal['product_id']
        }
        print('Sending order: ', order)
        coinbase_order = self.adapter.submit_order(order)
        if coinbase_order is None:
            print('Error coinbase_order as None')
        coinbase_order['signal_id'] = trade_signal['order_id']
        print('coinbase_order: ', coinbase_order)
        persist_order = Order(
            signal_id=trade_signal['order_id'],
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
