import time
import yfinance as yf
import pandas as pd
import utils
from Indicators import *
import constants

CRYPTO_EXCHANGE = 'CRYPTO'
ULTIMATE_INDICATOR = 'sma(close, 5) > sma(open, 5)'

class UltimateCalculator:

    @staticmethod
    def instance():
        return ultimateCalculator

    def __init__(self, awsUtils: utils.AwsUtils, mailingUtils: utils.MailingUtils) -> None:
        self._awsUtils = awsUtils
        self._mailingUtils = mailingUtils

    def run(self):
        cryptoSymbols = ['FIL-USD', 'RUNE-USD', 'XRP-USD', 'OP-USD', 'UNI-USD']

        signals = {}
        for symbol in cryptoSymbols:
            time.sleep(15)
            historicalData = yf.download(
                symbol,
                start=constants.CandlesConstants.CANDLES_ABS_START_DATE.value,
                end=constants.CandlesConstants.CANDLES_ABS_END_DATE.value
            )
            lastFiveSignals = self._getLastFiveSignals(historicalData)
            signals[symbol] = lastFiveSignals

        self._mailingUtils.sendUltimateCalculatorReport(signals)

        return {
            'success': True
        }

    def _getLastFiveSignals(self, df) -> []:
        data = pd.DataFrame(df).reset_index()
        data['Date'] = pd.to_datetime(data['Date'])

        (date, open, high, low, close, volume) = (
            data['Date'],
            data['Open'],
            data['High'],
            data['Low'],
            data['Close'],
            data['Volume']
        )

        return (
            [date.strftime('%Y-%m-%d') for date in data['Date'].apply(pd.to_datetime).dt.date.tolist()[-5:]],
            ['Buy' if value else 'Sell' for value in eval(ULTIMATE_INDICATOR)[-5:]]
        )

ultimateCalculator = UltimateCalculator(utils.AwsUtils.instance(), utils.MailingUtils.instance())
