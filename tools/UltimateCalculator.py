import time
import pandas as pd
from models import CalculateRequest
from providers.CandlesProvider import CandlesProvider
import utils
from Indicators import *

ULTIMATE_INDICATOR = 'sma(close, 3) > sma(open, 3)'

class UltimateCalculator:

    @staticmethod
    def instance():
        return ultimateCalculator

    def __init__(self) -> None:
        self._candlesProvider = CandlesProvider.instance()
        self._telegramUtils = utils.TelegramUtils.instance()

    def run(self):
        cryptoSymbols = ['FIL/USD', 'RUNE/USD', 'XRP/USD', 'OP/USD']

        for symbol in cryptoSymbols:
            time.sleep(5)
            request = CalculateRequest (
                type = "cryptocurrencies",
                userId = "",
                symbol = symbol,
                exchange = "",
                indicator = ULTIMATE_INDICATOR,
                apiKey = "e21a1ce91bfc46d79fa61834cfcedff3",
                interval = "4h",
                startDate = "2023-12-01"
            )
            historicalData = self._candlesProvider.getCandles(request)
            lastFiveSignals = self._getLastFiveSignals(historicalData)
            self._sendViaTelegram(symbol, lastFiveSignals)

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
            [value.strftime("%Y-%m-%d %H:%M:%S") for value in date.tolist()[-5:]],
            ['Buy' if value else 'Sell' for value in eval(ULTIMATE_INDICATOR)[-5:]]
        )

    def _sendViaTelegram(self, symbol, signals):
        telegramMessage = f"{symbol}\n\n"
        for i in range(5):
            telegramMessage += f"Time -> {str(signals[0][i])} | Signal -> {signals[1][i]}\n\n"
        self._telegramUtils.sendMessage(telegramMessage)

ultimateCalculator = UltimateCalculator()
