import json
import logging
from logging.config import fileConfig
import boto3
from config import aws as aws_config
from order.manager import OrderManager

# init logger
fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=aws_config['dev']['sqs']['queue-name'])
order_manager = OrderManager()

while True:
    messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=5)
    for message in messages:
        signal = json.loads(message.body)
        logger.info('Received message %s', signal)
        order_manager.process(signal)
        message.delete()
