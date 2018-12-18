import argparse

from algotrader.logging import setup_logging
from algotrader import logger


def main():
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
