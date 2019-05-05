from mongoengine import (StringField,
                         DateTimeField,
                         BooleanField,
                         DecimalField,
                         Document,
                         IntField,
                         LongField,
                         EmbeddedDocument,
                         EmbeddedDocumentListField
                         )


class Candle(Document):
    time = IntField(required=True)
    low = DecimalField(required=True)
    high = DecimalField(required=True)
    open = DecimalField(required=True)
    close = DecimalField(required=True)
    volume = DecimalField(required=True)
    interval = IntField(required=True)
    product_id = StringField(required=True)

    meta = {'collection': 'candles'}
