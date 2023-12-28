from models import IndicatorTestRecord
from providers.CandlesProvider import CandlesProvider
from Indicators import *
from models.CalculateRequest import CalculateRequest
from utils import AwsUtils, ModelUtils

class CalculateHandler:

    @staticmethod
    def instance():
        return calculateHandler

    def __init__(self) -> None:
        self._candlesProvider = CandlesProvider.instance()
        self._awsUtils = AwsUtils.instance()

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

        profitPercentage = round(((cash - request.cash) / request.cash) * 100.0, 2)
        self._storeTestData(request, profitPercentage, actions)

        return {
            'start': str(date.tolist()[0]).split(' ')[0],
            'end': str(date.tolist()[-1]).split(' ')[0],
            'cash': cash,
            'actions': actions,
            'profit': request.cash - cash,
            'profitPercentage': profitPercentage,
            'success': True
        }

    def _storeTestData(self, request: CalculateRequest, profitPercentage: float, actions: []):
        indicatorTestRecord = IndicatorTestRecord(
            userId=request.userId,
            timestamp=request.timestamp,
            symbol=request.symbol,
            indicator=request.indicator,
            interval=request.interval,
            startDate=request.startDate,
            endDate=request.endDate,
            profit=str(profitPercentage)
        )
        self._awsUtils.addIndicatorTest(ModelUtils.toJson(indicatorTestRecord))
        self._awsUtils.addIndicatorTestActions(
            userId=request.userId,
            timestamp=request.timestamp,
            symbol=request.symbol,
            actions=actions
        )

calculateHandler = CalculateHandler()