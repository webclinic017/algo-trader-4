import json
import boto3

from algotrader.config import aws as aws_config
from algotrader.order.manager import OrderManager
from algotrader import logger


sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=aws_config['sqs']['queue-name'])
order_manager = OrderManager()

while True:
    messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=5)
    for message in messages:
        signal = json.loads(message.body)
        logger.info('Received message %s', signal)
        order_manager.process(signal)
        message.delete()
