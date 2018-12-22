from algotrader.order.manager import OrderManager
from algotrader.signal.file import SourceFile
from algotrader.signal.sqs import SourceSQS


class Receiver():

    def __init__(self, storage, exchange, source, filename=None):
        self.order_manager = OrderManager(storage, exchange)
        self.source_dict = {
            'sqs': SourceSQS,
            'file': SourceFile,
        }
        self.filename = filename
        self.source = source
        self._get_source()

    def _get_source(self):
        source_cls = self.source_dict[self.source]
        if self.source == 'file':
            self.source = source_cls(self.order_manager, filename=self.filename)
        elif self.source == 'sqs':
            self.source = source_cls()

    # TODO: Re-consider signal structure. Remove duplications, rename order_id to signal_id etc.
    def consume(self):
        """
            Process the given signal.
            Example signal;
            {
                "order_id": "ETH-USD_coinbase_1543359420",
                "product_id": "ETH-USD",
                "type": "market",
                "side": "sell",
                "size": "all"
            }
        """
        self.source.consume()
