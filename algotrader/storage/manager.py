
from algotrader.logging import logger
from algotrader.signal import TradeSignal, TradeOrder
from algotrader.storage.mongodb import MongoDB


# TODO: Transform return result into a common class.
class StorageManager():
    def __init__(self, storage):
        # TODO: Add new storage types.
        # TODO: Should be constant.
        if storage == 'mongodb':
            self.storage = MongoDB()

    def create_signal(self, trade_signal: TradeSignal):
        logger.info('Creating signal %s', trade_signal)
        self.storage.create_signal(trade_signal)

    def create_order(self, trade_order: TradeOrder):
        logger.info('Creating order %s', trade_order)
        self.storage.create_order(trade_order)

    def get_orders(self, statuses: list):
        return self.storage.get_orders(statuses)

    # TODO: Reconsider params.
    def update_order(self, _id, fills, status):
        self.storage.update_order(_id, fills, status)
