import argparse

from algotrader.logging import setup_logging
from algotrader import logger
from algotrader.signal.receiver import Receiver


def main():
    # TODO: Add source argument such as SQS or file (for test purposes)
    # TODO: Add target argument such as mongodb, mysql, redis etc.
    parser = argparse.ArgumentParser()
    parser.add_argument('--logging-level',
                        default='info',
                        choices=['debug', 'info', 'warning', 'error'],
                        type=str.lower,
                        help='Print logs')
    args = parser.parse_args()

    setup_logging(args.logging_level)

    logger.info('Consuming signals..')

    receiver = Receiver()
    while True:
        receiver.consume()


if __name__ == '__main__':
    main()
