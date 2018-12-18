import argparse

from algotrader.logging import setup_logging
from algotrader import logger


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

    logger.debug('debug')
    logger.info('info')
    logger.error('error')


if __name__ == '__main__':
    main()
