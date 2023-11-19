# To set the project directory
import os
import sys
import re

current_script_path = os.path.abspath(__file__)
project_directory = os.path.dirname(os.path.dirname(current_script_path))
sys.path.append(project_directory)

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from IndicatorCalculator.Indicators import *
from CandlesManager.CandlesProvider import CandlesProvider

# Constants
INDICATOR_PATTERN = r'^[a-zA-Z0-9,()+\-*/|&<>= ]+$'

# Define the needed objects
app = FastAPI()
candlesProvider = CandlesProvider()

class Calculate(BaseModel):
    symbol: str
    indicator: str
    cash: float = Field(1000.0)
    startDate: str = Field('2000-01-01')
    endDate: str = Field('2029-12-31')

# Calculate endpoint which calculate the given indicator on the given symbol and finds the current amount of money if the user
# followed the indicator starting with $1000 cash
@app.post('/calculate')
async def calculate(calculate: Calculate):
    if not re.match(INDICATOR_PATTERN, calculate.indicator):
        raise HTTPException(status_code = 403, detail = 'Invalid indicator')

    data = candlesProvider.getCandles(calculate.symbol, calculate.startDate, calculate.endDate)
    mdata = data.copy()
    date = data.copy()['Date']
    volume = data.copy()['Volume']
    open, high, low, close = data.copy()['Open'], data.copy()['High'], data.copy()['Low'], data.copy()['Close']
    buySellSignals = eval(calculate.indicator)

    cash, stocks, preSignal, startSignal = calculate.cash, 0, False, next((i for i, value in enumerate(buySellSignals) if value), None)

    actions = []

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
                        'cach': cash
                    })
                else:
                    cash = stocks * close[index]
                    stocks = 0
                    actions.append({
                        'date': date[index],
                        'price': close[index],
                        'action': 'sell',
                        'stocks': stocks,
                        'cach': cash
                    })
                preSignal = signal
        if preSignal:
            cash = stocks * close[index]
            stocks = 0

    return {
        'start': date.tolist()[0],
        'end': date.tolist()[-1],
        'cash': cash,
        'actions': actions
    }

# Run FastApi server when executing this file
if __name__ == "__main__":
    uvicorn.run("main:app", port=3010, reload=True)