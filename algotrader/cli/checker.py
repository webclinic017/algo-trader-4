import argparse
import time

from algotrader.logging import setup_logging
from algotrader import logger
from algotrader.order.order_checker import OrderChecker


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
    order_checker = OrderChecker()
    while True:
        order_checker.check_orders()
        logger.info('Sleeping for 5 seconds...')
        time.sleep(5)


if __name__ == '__main__':
    main()
