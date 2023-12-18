import time
import pandas as pd
from models import CalculateRequest
from providers.CandlesProvider import CandlesProvider
import utils
from Indicators import *

ULTIMATE_INDICATOR = 'sma(close, 5) > sma(open, 5)'

class UltimateCalculator:

    @staticmethod
    def instance():
        return ultimateCalculator

    def __init__(self) -> None:
        self._candlesProvider = CandlesProvider.instance()
        self._mailingUtils = utils.MailingUtils.instance()

    def run(self):
        cryptoSymbols = ['FIL/USD', 'RUNE/USD', 'XRP/USD', 'OP/USD', 'DOGE/USD', 'MATIC/USD']

        signals = {}
        for symbol in cryptoSymbols:
            time.sleep(3)
            request = CalculateRequest (
                type = "cryptocurrencies",
                userId = "auth0|65683f9089d738e2258d3080",
                symbol = symbol,
                exchange = "",
                indicator = ULTIMATE_INDICATOR,
            )
            historicalData = self._candlesProvider.getCandles(request, "e21a1ce91bfc46d79fa61834cfcedff3")
            lastFiveSignals = self._getLastFiveSignals(historicalData)
            signals[symbol] = lastFiveSignals

        self._mailingUtils.sendUltimateCalculatorReport(signals)

        return {
            'success': True
        }

    def _getLastFiveSignals(self, df) -> []:
        data = pd.DataFrame(df).reset_index()
        data['Date'] = pd.to_datetime(data['Date'])

        (date, open, high, low, close) = (
            data['Date'],
            data['Open'],
            data['High'],
            data['Low'],
            data['Close']
        )

        return (
            [date.strftime('%Y-%m-%d') for date in data['Date'].apply(pd.to_datetime).dt.date.tolist()[-5:]],
            ['Buy' if value else 'Sell' for value in eval(ULTIMATE_INDICATOR)[-5:]]
        )

ultimateCalculator = UltimateCalculator()
