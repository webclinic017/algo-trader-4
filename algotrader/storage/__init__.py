

# TODO: Raise NotImplementedError
class StorageBase():

    def __init__(self, database):
        pass

    def create_signal(self):
        raise NotImplementedError("Subclasses should implement this!")

    def create_order(self):
        raise NotImplementedError("Subclasses should implement this!")

    def get_orders(self, status: list):
        raise NotImplementedError("Subclasses should implement this!")

    def update_order(self, _id: int, fills: list, status: str):
        raise NotImplementedError("Subclasses should implement this!")
