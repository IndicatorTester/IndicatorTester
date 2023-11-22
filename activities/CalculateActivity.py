import re
from fastapi import HTTPException
from handlers.CalculateHandler import CalculateHandler
from models.CalculateRequest import CalculateRequest

INDICATOR_PATTERN = r'^[a-zA-Z0-9,()+\-*/|&<>=. ]+$'

calculateHandler = CalculateHandler()

# Calculate endpoint which calculate the given indicator on the given symbol and finds the current amount of money if the user
# followed the indicator starting with X amount of cash
class CalculateActivity:
    @classmethod
    def act(cls, request: CalculateRequest):
        if request.exchange is None:
            raise HTTPException(status_code = 403, detail = 'Exchange can\'t be null')
        if request.interval is None:
            raise HTTPException(status_code = 403, detail = 'Interval can\'t be null')
        if request.symbol is None:
            raise HTTPException(status_code = 403, detail = 'Symbol can\'t be null')
        if request.indicator is None:
            raise HTTPException(status_code = 403, detail = 'Indicator can\'t be null')
        if request.cash <= 0:
            raise HTTPException(status_code = 403, detail = 'Cash must be a positive number')
        if not re.match(INDICATOR_PATTERN, request.indicator):
            raise HTTPException(status_code = 403, detail = 'Invalid indicator')

        try:
            return calculateHandler.handle(request)
        except NameError as ne:
            raise HTTPException(status_code = 403, detail = 'Unsupported indicator')
        except Exception as e:
            raise HTTPException(status_code = 500, detail = 'Something went wrong')