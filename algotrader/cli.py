import time
import argparse

from algotrader import logger
from algotrader.config import load_config
from algotrader.logging import setup_logging
from algotrader.signal.receiver import Receiver
from algotrader.order.manager import OrderManager
from algotrader.storage.manager import StorageManager


def main():
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
    parser.add_argument('--database',
                        choices=StorageManager.storage_types.keys(),
                        help='Database',
                        default='mongodb')
    parser.add_argument('--signal-source',
                        choices=Receiver.source_dict.keys(),
                        help='Signal source',
                        default='sqs')
    parser.add_argument('--source-filename',
                        help='JSON formatted file as a file source')
    parser.add_argument('--log-file', help='Log file name')
    parser.add_argument('--config-file',
                        type=str.lower,
                        help='Config file')
    parser.add_argument('--exchange',
                        help='Exchange check orders',
                        choices=OrderManager.exchange_dict.keys(),
                        type=str.lower,
                        default='coinbase')
    args = parser.parse_args()

    # Logging setup
    setup_logging(args.logging_level, filename=args.log_file)

    # Load config file
    load_config(args.config_file)

    # Create storage manager.
    storage_manager = StorageManager(storage=args.database)

    logger.info('Starting storage => %s', storage_manager)
    logger.info('Exchange => %s', args.exchange)
    logger.info('Signal source => %s', args.signal_source)

    if args.worker == 'signal-consumer':
        logger.info('Starting signal consumer...')
        receiver = Receiver(storage_manager, args.exchange, args.signal_source, filename=args.source_filename)
        receiver.consume()
        logger.info('Exiting..')
        return

    if args.worker == 'order-checker':
        logger.info('Starting order checker...')
        order_manager = OrderManager(storage_manager, args.exchange)
        while True:
            order_manager.check_orders()
            logger.info('Sleeping for 5 seconds...')
            time.sleep(5)

        logger.info('Exiting..')
        return


if __name__ == '__main__':
    main()
