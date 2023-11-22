from providers.CandlesProvider import CandlesProvider
from Indicators import *
from models.CalculateRequest import CalculateRequest

candlesProvider = CandlesProvider()

class CalculateHandler:
    @classmethod
    def handle(cls, request: CalculateRequest):
        data = candlesProvider.getCandles(request.exchange, request.interval, request.symbol)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.set_index('Date').loc[request.startDate : request.endDate].reset_index()

        (date, open, high, low, close, volume) = (
            data['Date'],
            data['Open'],
            data['High'],
            data['Low'],
            data['Close'],
            data['Volume']
        )

        buySellSignals = eval(request.indicator)

        (cash, stocks, preSignal, startSignal, actions) = (
            request.cash,
            0,
            False, 
            next((i for i, value in enumerate(buySellSignals) if value), None),
            []
        )

        if startSignal is not None:
            for index, signal in enumerate(buySellSignals[startSignal:]):
                if signal != preSignal:
                    if signal:
                        stocks = cash / close[index]
                        cash = 0
                        actions.append({
                            'date': date[index],
                            'price': close[index],
                            'action': 'buy',
                            'stocks': stocks,
                            'cash': cash
                        })
                    else:
                        cash = stocks * close[index]
                        stocks = 0
                        actions.append({
                            'date': date[index],
                            'price': close[index],
                            'action': 'sell',
                            'stocks': stocks,
                            'cash': cash
                        })
                    preSignal = signal
            if preSignal:
                cash = stocks * close[index]
                stocks = 0

        return {
            'start': date.tolist()[0],
            'end': date.tolist()[-1],
            'cash': cash,
            'actions': actions,
            'success': True
        }