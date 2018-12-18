
class CommonUtils():

    @staticmethod
    def get_base_currency(trading_pair):
        return trading_pair.split('-')[0].lower()

    @staticmethod
    def get_quote_currency(trading_pair):
        return trading_pair.split('-')[1].lower()
