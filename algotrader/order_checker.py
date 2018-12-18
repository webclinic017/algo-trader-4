from pymongo import MongoClient

from algotrader.order.manager import OrderManager


client = MongoClient('localhost', 27017)
db = client['algorading']
orders = db['orders']

order_manager = OrderManager()
while True:
    for o in orders.find({'$or': [{'status': 'pending'}, {'status': 'open'}]}):
        order_result = order_manager.get_order(o)
        order_manager.give_decision(order_result)
