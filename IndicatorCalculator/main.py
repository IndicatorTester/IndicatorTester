# To set the project directory
import os
import sys

current_script_path = os.path.abspath(__file__)
project_directory = os.path.dirname(os.path.dirname(current_script_path))
sys.path.append(project_directory)

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from IndicatorCalculator.Indicators import *
from CandlesManager.CandlesProvider import CandlesProvider

# Define the needed objects
app = FastAPI()
candlesProvider = CandlesProvider()

class Calculate(BaseModel):
    symbol: str
    indicator: str

# Calculate endpoint which calculate the given indicator on the given symbol and finds the current amount of money if the user
# followed the indicator starting with $1000 cash
@app.post('/calculate')
async def calculate(calculate: Calculate):
    data = candlesProvider.getCandles(calculate.symbol)
    time, open, high, low, close = data['t'], data['o'], data['h'], data['l'], data['c']
    buySellSignals = eval(calculate.indicator)

    cash, stocks, preSignal, startSignal = 1000.0, 0, False, next((i for i, value in enumerate(buySellSignals) if value), None)

    if startSignal is not None:
        for index, signal in enumerate(buySellSignals[startSignal:]):
            if signal != preSignal:
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
        'start': datetime.utcfromtimestamp(data['t'][0]).strftime('%d/%b/%Y'),
        'end': datetime.utcfromtimestamp(data['t'][-1]).strftime('%d/%b/%Y'),
        'cash': cash
    }

# Run FastApi server when executing this file
if __name__ == "__main__":
    uvicorn.run("main:app", port=3010, reload=True)