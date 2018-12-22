from pymongo import MongoClient

from algotrader.storage import BaseStorage
from algotrader.storage.mongodb.models import Signal, Order


class MongoDB(BaseStorage):

    def __init__(self):
        # TODO: Should be config and param.
        self.host = 'localhost'
        self.port = 27017
        self.db = 'algotrader'
        self.collection = 'orders'

        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db]
        self.orders = self.db[self.collection]

    def __repr__(self):
        return 'MongoDB <Host: %s , Port: %s, Collection: %s>' % (self.host, self.port, self.collection)

    def create_signal(self, trade_signal):
        signal = Signal(signal_id=trade_signal.signal_id,
                        product_id=trade_signal.product_id,
                        order_type=trade_signal.order_type,
                        side=trade_signal.side,
                        size=trade_signal.size)
        signal.save()

    def create_order(self, trade_order):
        order = Order(
            signal_id=trade_order.order_id,
            order_id=trade_order.id,  # TODO: Coinbase specific. Make this more generic.
            price=trade_order.price,
            side=trade_order.side,
            size=trade_order.size,
            product_id=trade_order.product_id,
            created_at=trade_order.created_at,
            done_at=trade_order.done_at,
            status=trade_order.status,
            type=trade_order.type,
        )
        order.save()

    def get_orders(self, statuses: list):
        expr = [{'status': status} for status in statuses]
        return self.orders.find({'$or': expr})

    def update_order(self, _id, fills, status):
        self.orders.update(
            {'order_id': _id},
            {'$push': {'fills': {'$each': fills}}, '$set': {'status': status}}
        )
