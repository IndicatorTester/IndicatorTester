import pandas as pd
import constants
from Indicators import *
from models import CalculateExchangeRequest
from providers.CandlesProvider import CandlesProvider
from utils import AwsUtils

class CalculateExchangeHandler:

    @staticmethod
    def instance():
        return calculateExchangeHandler

    def __init__(self, candlesProvider: CandlesProvider, awsUtils: AwsUtils) -> None:
        self._candlesProvider = candlesProvider
        self._awsUtils = awsUtils

    def handle(self, request: CalculateExchangeRequest):
        exchangeSymbols = self._awsUtils.getDynamoItemsBySortKey(
            constants.AwsConstants.SYMBOLS_TABLE.value,
            constants.AwsConstants.SYMBOLS_TABLE_EXCHANGE_FIELD.value,
            request.exchange
        )

        response = []
        for symbolData in exchangeSymbols:
            try:
                print(symbolData['symbol'])
                response.append(self._calculateSymbol(symbolData['symbol'], request))
            except Exception as e:
                response.append({
                    'symbol': symbolData['symbol'],
                    'cash': 1000.0,
                    'success': False
                })

        return response

    def _calculateSymbol(self, symbol, request: CalculateExchangeRequest):
        data = self._candlesProvider.getCandles(request.exchange, request.interval, symbol)
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

        (cash, stocks, preSignal, startSignal) = (
            request.cash,
            0,
            False, 
            next((i for i, value in enumerate(buySellSignals) if value), None)
        )

        if startSignal is not None:
            for index, signal in enumerate(buySellSignals[startSignal:]):
                if signal != preSignal:
                    if close[index] == 0:
                        continue
                    if signal:
                        stocks = cash / close[index]
                        cash = 0
                    else:
                        cash = stocks * close[index]
                        stocks = 0
                    preSignal = signal
            if preSignal:
                cash = stocks * close[index]
                stocks = 0

        return {
            'symbol': symbol,
            'cash': cash,
            'success': True
        }

calculateExchangeHandler = CalculateExchangeHandler(CandlesProvider.instance(), AwsUtils.instance())