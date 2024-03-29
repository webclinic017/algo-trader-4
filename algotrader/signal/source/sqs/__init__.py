import json
import boto3

from algotrader.signal import TradeSignal
from algotrader.config import config
from algotrader import logger


class SourceSQS():
    def __init__(self, order_manager):
        self.order_manager = order_manager
        sqs = boto3.resource('sqs')
        self.queue = sqs.get_queue_by_name(QueueName=config['aws']['sqs']['queue-name'])

    def consume(self):
        while True:
            messages = self.queue.receive_messages(MaxNumberOfMessages=config['aws']['sqs']['max_number_of_messages'],
                                                   WaitTimeSeconds=config['aws']['sqs']['wait_time_seconds'])
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
