import json
import boto3

from algotrader.config import aws as aws_config
from algotrader.order.manager import OrderManager
from algotrader.trade_signal import TradeSignal
from algotrader import logger


class Receiver():

    def __init__(self):
        sqs = boto3.resource('sqs')
        self.queue = sqs.get_queue_by_name(QueueName=aws_config['sqs']['queue-name'])
        self.order_manager = OrderManager()

    # TODO: Re-consider signal structure. Remove duplications, rename order_id to signal_id etc.
    def consume(self):
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
        # TODO: Params should be a config.
        messages = self.queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=5)
        for message in messages:
            signal_dict = json.loads(message.body)
            logger.info('Received message %s', signal_dict)

            trade_signal = TradeSignal(signal_id=signal_dict['order_id'],
                                       product_id=signal_dict['product_id'],
                                       order_type=signal_dict['type'],
                                       side=signal_dict['side'],
                                       size=signal_dict['size'])

            self.order_manager.process(trade_signal)
            message.delete()
