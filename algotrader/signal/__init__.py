

class TradeSignal():

    BUY_SIDE = 'buy'

    def __init__(self, signal_id=None, product_id=None, order_type=None, side=None, size=None):
        self._signal_id = signal_id
        self._product_id = product_id
        self._order_type = order_type
        self._side = side
        self._size = size
        self._process_curencies()

    def __repr__(self):
        return 'TradeSignal <ID: %s , Product-ID: %s, Order-Type: %s, Side: %s, Size: %s>' % (self._signal_id,
                                                                                              self._product_id,
                                                                                              self._order_type,
                                                                                              self._side,
                                                                                              self._size)

    def _process_curencies(self):
        self.base_currency, self.quote_currency = self.product_id.lower().split('-')

    @property
    def order_type(self):
        return self._order_type

    @property
    def signal_id(self):
        return self._signal_id

    @property
    def side(self):
        return self._side

    @property
    def product_id(self):
        return self._product_id

    @property
    def size(self):
        return self._size

    @property
    def currency(self):
        if self.side == self.BUY_SIDE:
            return self.quote_currency

        return self.base_currency


# TODO: Too generic name, rename it.
class TradeOrder():

    # TODO: Too many params.
    def __init__(self, order_id, price, side, size, product_id, created_at, done_at, status, _type):
        self.signal_id = order_id
        self.price = price
        self.side = side
        self.size = size
        self.product_id = product_id
        self.created_at = created_at
        self.done_at = done_at
        self.status = status
        self.type = _type

    def __repr__(self):
        return 'TradeOrder <Signal-ID: %s , Price: %s, Product-ID: %s, CreatedAt: %s, DoneAt: %s>' % (self.signal_id,
                                                                                                      self.price,
                                                                                                      self.product_id,
                                                                                                      self.created_at,
                                                                                                      self.done_at)
