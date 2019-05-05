from mongoengine import connect
from pymongo import MongoClient

from algotrader.storage import BaseStorage
from algotrader.storage.mongodb.models import Signal, Order
from algotrader.config import config
from algotrader.backtesting.models import Candle


class MongoDB(BaseStorage):

    def __init__(self):
        connect('algotrader')
        self.host = config['db']['mongodb']['host']
        self.port = config['db']['mongodb']['port']
        self.database = config['db']['mongodb']['database']
        client = MongoClient(self.host, self.port)
        self.db = client.get_database(self.database)

    def __repr__(self):
        return 'MongoDB <Host: %s , Port: %s, Database: %s>' % (self.host, self.port, self.database)

    def create_signal(self, trade_signal):
        signal = Signal(signal_id=trade_signal.signal_id,
                        product_id=trade_signal.product_id,
                        order_type=trade_signal.order_type,
                        side=trade_signal.side,
                        size=trade_signal.size)
        signal.save()

    def create_order(self, trade_order):
        order = Order(
            signal_id=trade_order.signal_id,
            order_id=trade_order.order_id,  # TODO: Coinbase specific. Make this more generic.
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
        orders = self.db.get_collection('orders')
        return orders.find({'$or': expr})

    def get_signals(self):
        signals = self.db.get_collection('signals')
        return signals.find()

    def update_order(self, order_id, fills, status):
        orders = self.db.get_collection('orders')
        orders.update(
            {'order_id': order_id},
            {'$push': {'fills': {'$each': fills}}, '$set': {'status': status}}
        )

    def create_candle(self, time, low, high, open, close, volume, product_id, interval):
        candle = Candle(
            time=time,
            low=low,
            high=high,
            open=open,
            close=close,
            volume=volume,
            product_id=product_id,
            interval=interval
        )
        candle.save()

    def get_max_candle_by_time(self, product_id):
        candles = self.db.get_collection('candles')
        cursor = candles.find().sort([('time', -1)])
        try:
            return cursor.next()
        except StopIteration:
            return
