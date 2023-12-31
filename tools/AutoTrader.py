import time
import pandas as pd
from accessors import BybitAccessor, TelegramAccessor
from models import CalculateRequest
from providers.CandlesProvider import CandlesProvider
from Indicators import *
import logging

BUY_SIGNAL = 'Buy'
SELL_SIGNAL = 'Sell'
TRADING_INTERVAL = '1h'
TRADING_INDICATOR = 'sma(close, 2) > sma(open, 2)'
DATA_PROVIDER_KEY = 'e21a1ce91bfc46d79fa61834cfcedff3'
SYMBOLS = ['DOGE/USD', 'MATIC/USD', 'FIL/USD', 'RUNE/USD', 'XRP/USD', 'OP/USD']

class AutoTrader:

    @staticmethod
    def instance():
        return autoTrader

    def __init__(self) -> None:
        self._candlesProvider = CandlesProvider.instance()
        self._bybitAccessor = BybitAccessor.instance()
        self._telegramAccessor = TelegramAccessor.instance()

    def trade(self):
        for symbol in SYMBOLS:
            time.sleep(10)
            try :
                request = CalculateRequest (
                    type = "cryptocurrencies",
                    userId = "",
                    symbol = symbol,
                    exchange = "",
                    indicator = TRADING_INDICATOR,
                    apiKey = DATA_PROVIDER_KEY,
                    interval = TRADING_INTERVAL,
                    startDate = "2023-12-01"
                )
                historicalData = self._candlesProvider.getCandles(request)
                signals = self._calculateSymbolSignals(symbol, historicalData)

                tradeResult = self._bybitAccessor.trade(symbol, signals[-2])
                self._telegramAccessor.sendMessage(
                    f"{signals[-1]} action on symbol: {symbol}, Result -> {tradeResult}"
                )
            except Exception as e:
                logging.error(f"An error occurred on AutoTrader with symbol: {symbol} -> {str(e)}", e)
                self._telegramAccessor.sendMessage(
                    f"An error occurred on AutoTrader with symbol: {symbol} -> {str(e)}"
                )

        return {
            "success": True
        }

    def _calculateSymbolSignals(self, symbol: str, historicalData: pd.DataFrame):
        data = pd.DataFrame(historicalData).reset_index()
        data['Date'] = pd.to_datetime(data['Date'])

        (date, open, high, low, close) = (
            data['Date'],
            data['Open'],
            data['High'],
            data['Low'],
            data['Close']
        )

        times = [value.strftime("%Y-%m-%d %H:%M:%S") for value in date.tolist()[-5:]]
        signals = [BUY_SIGNAL if value else SELL_SIGNAL for value in eval(TRADING_INDICATOR)[-5:]]

        logging.info(f"Calculated symbol signals: {symbol}. Signals: {signals}, times: {times}")

        return signals

autoTrader = AutoTrader()