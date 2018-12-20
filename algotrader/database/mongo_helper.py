from mongoengine import (StringField,
                         DateTimeField,
                         BooleanField,
                         Document,
                         connect,
                         EmbeddedDocument,
                         EmbeddedDocumentListField
                         )

connect('algotrader')


class Signal(Document):
    signal_id = StringField(required=True)
    product_id = StringField(required=True)
    order_type = StringField(required=True)
    side = StringField(required=True)
    size = StringField(required=True)

    meta = {'collection': 'signals'}


class Fill(EmbeddedDocument):
    trade_id = StringField()
    product_id = StringField()
    price = StringField()
    size = StringField()
    order_id = StringField()
    created_at = DateTimeField()
    liquidity = StringField()
    fee = StringField()
    settled = BooleanField()
    side = StringField()


class Order(Document):
    signal_id = StringField(required=True)
    order_id = StringField()
    price = StringField()
    size = StringField()
    side = StringField()
    created_at = DateTimeField()
    done_at = DateTimeField()
    status = StringField()
    type = StringField()
    product_id = StringField()
    fills = EmbeddedDocumentListField(Fill, default=[])

    meta = {'collection': 'orders', 'strict': False}
