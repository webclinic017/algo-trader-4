

# TODO: Raise NotImplementedError
class StorageBase():

    def __init__(self, database):
        pass

    def create_signal(self):
        pass

    def create_order(self):
        pass

    def get_orders(self, status: list):
        pass

    def update_order(self, _id: int, fills: list, status: str):
        pass
