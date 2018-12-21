import argparse
import time

from algotrader import logger
from algotrader.logging import setup_logging
from algotrader.order.order_checker import OrderChecker
from algotrader.storage.manager import StorageManager


def main():
    # TODO: Add source argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--logging-level',
                        default='info',
                        choices=['debug', 'info', 'warning', 'error'],
                        type=str.lower,
                        help='Print logs')
    args = parser.parse_args()

    setup_logging(args.logging_level)

    logger.debug('debug')
    logger.info('info')
    logger.error('error')

    # TODO: DRY: Merge CLI files.
    # TODO: make this constant
    # TODO: Should be a param.
    storage = 'mongodb'
    storage_manager = StorageManager(storage)

    order_checker = OrderChecker(storage_manager)
    while True:
        order_checker.check_orders()
        logger.info('Sleeping for 5 seconds...')
        time.sleep(5)


if __name__ == '__main__':
    main()
