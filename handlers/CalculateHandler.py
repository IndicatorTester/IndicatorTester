from providers.CandlesProvider import CandlesProvider
from Indicators import *
from models.CalculateRequest import CalculateRequest

class CalculateHandler:

    @staticmethod
    def instance():
        return calculateHandler

    def __init__(self) -> None:
        self._candlesProvider = CandlesProvider.instance()

    def handle(self, request: CalculateRequest):
        data = self._candlesProvider.getCandles(request)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.set_index('Date').loc[request.startDate : request.endDate].reset_index()

        (date, open, high, low, close) = (
            data['Date'],
            data['Open'],
            data['High'],
            data['Low'],
            data['Close']
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
                    if close[index] == 0:
                        continue
                    if signal:
                        stocks = cash / close[index]
                        cash = 0
                        actions.append({
                            'date': str(date[index]),
                            'price': close[index],
                            'action': 'buy',
                            'stocks': stocks,
                            'cash': cash
                        })
                    else:
                        cash = stocks * close[index]
                        stocks = 0
                        actions.append({
                            'date': str(date[index]),
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
            'start': str(date.tolist()[0]).split(' ')[0],
            'end': str(date.tolist()[-1]).split(' ')[0],
            'cash': cash,
            'actions': actions,
            'success': True
        }

calculateHandler = CalculateHandler()