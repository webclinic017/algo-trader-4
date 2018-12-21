import argparse

from algotrader import logger
from algotrader.logging import setup_logging
from algotrader.signal.receiver import Receiver
from algotrader.storage.manager import StorageManager


def main():
    # TODO: Add source argument such as SQS or file (for test purposes)
    # TODO: Add target storage argument such as mongodb, mysql, redis etc.
    parser = argparse.ArgumentParser()
    parser.add_argument('--logging-level',
                        default='info',
                        choices=['debug', 'info', 'warning', 'error'],
                        type=str.lower,
                        help='Print logs')
    args = parser.parse_args()

    setup_logging(args.logging_level)

    logger.info('Consuming signals..')

    # TODO: DRY: Merge CLI files.
    # TODO: make this constant
    # TODO: Should be a param.
    storage = 'mongodb'
    storage_manager = StorageManager(storage)

    receiver = Receiver(storage_manager)
    while True:
        receiver.consume()


if __name__ == '__main__':
    main()
