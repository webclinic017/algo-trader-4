import json

from algotrader import logger
from algotrader.signal import TradeSignal


class SourceFile():
    def __init__(self, order_manager, filename):
        self.order_manager = order_manager
        self.filename = filename

    def consume(self):
        with open(self.filename, 'r') as f:
            signal_dict = json.load(f)
            logger.info('Received signal: %s', signal_dict)

            # TODO: DRY
            trade_signal = TradeSignal(signal_id=signal_dict['order_id'],
                                       product_id=signal_dict['product_id'],
                                       order_type=signal_dict['type'],
                                       side=signal_dict['side'],
                                       size=signal_dict['size'])

            self.order_manager.process(trade_signal)
