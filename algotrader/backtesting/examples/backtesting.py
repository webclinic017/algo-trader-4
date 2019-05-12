from datetime import datetime
import backtrader as bt
from mongoengine import connect
from pymongo import MongoClient
import pandas as pd
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo


class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 13),
        ('printlog', True)
        )

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED, price: %.2f, cost: %.2f, comm: %.2f" % 
                        (order.executed.price,
                         order.executed.value,
                         order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log("SELL EXECUTED, price: %.2f, cost: %.2f, comm: %.2f" % 
                        (order.executed.price,
                         order.executed.value,
                         order.executed.comm))
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" %
                (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log("Close, %.2f" % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.log("BUY CREATE, %.2f" % self.dataclose[0])
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                self.log("SELL CREATE, %.2f" % self.dataclose[0])
                self.order = self.sell()

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' % (self.params.maperiod, self.broker.getvalue()), doprint=True)


class OHLCData(bt.feeds.GenericCSVData):
    params = (
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', -1),
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 60),
    )


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    cerebro.broker.setcommission(commission=0.001)

    connect('algotrader')
    client = MongoClient()
    db = client.get_database('algotrader')
    candles = db.get_collection('candles')
    candle_data = candles.find().sort([('time', 1)])

    ohlc = []
    for candle in candle_data:
        ohlc.append([datetime.utcfromtimestamp(candle['time']),
                                               candle['open'],
                                               candle['high'],
                                               candle['low'],
                                               candle['close'],
                                               candle['volume']])

    df = pd.DataFrame(ohlc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df.to_csv('/Users/buraktas/algotrader/algotrader/backtesting/examples/test_data.csv', index=False)
    data = OHLCData(dataname='/Users/buraktas/algotrader/algotrader/backtesting/examples/test_data.csv')

    cerebro.adddata(data)
    cerebro.broker.setcash(10000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    b = Bokeh(style='bar', plot_mode='single')
    cerebro.plot(b)
