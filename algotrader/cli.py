import time
import argparse

from algotrader import logger
from algotrader.logging import setup_logging
from algotrader.signal.receiver import Receiver
from algotrader.order.order_checker import OrderChecker
from algotrader.storage.manager import StorageManager


def main():
    # TODO: Add source argument such as SQS or file (for test purposes)
    parser = argparse.ArgumentParser()
    parser.add_argument('--logging-level',
                        default='info',
                        choices=['debug', 'info', 'warning', 'error'],
                        type=str.lower,
                        help='Print logs')
    parser.add_argument('--worker',
                        choices=['signal-consumer', 'order-checker'],
                        type=str.lower,
                        help='Workers')
    parser.add_argument('--database', help='Database', default='mongodb')  # TODO: make this constant.
    parser.add_argument('--exchange',
                        help='Exchange check orders',
                        choices='coinbase',
                        type=str.lower,
                        default=['coinbase'])  # TODO: Make this constant. (Should be a list of exchanges)
    args = parser.parse_args()

    setup_logging(args.logging_level)

    # Create storage manager.
    storage_manager = StorageManager(storage=args.database)
    logger.info('Starting storage => %s', storage_manager)
    logger.info('Exchange => %s', args.exchange)

    # TODO: should be more readable.
    if args.worker == 'signal-consumer':
        logger.info('Starting signal consumer...')
        receiver = Receiver(storage_manager, args.exchange)
        while True:
            receiver.consume()
    elif args.worker == 'order-checker':
        logger.info('Starting order checker...')
        order_checker = OrderChecker(storage_manager, args.exchange)
        while True:
            order_checker.check_orders()
            logger.info('Sleeping for 5 seconds...')
            time.sleep(5)


if __name__ == '__main__':
    main()