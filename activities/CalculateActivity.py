import re
from fastapi import HTTPException
from errors.DataProviderError import DataProviderError
from errors.TestError import TestError
from handlers.CalculateHandler import CalculateHandler
from models.CalculateRequest import CalculateRequest
import logging

INDICATOR_PATTERN = r'^[a-zA-Z0-9,()+\-*/|&<>=.! ]+$'

class CalculateActivity:

    @staticmethod
    def instance():
        return calculateActivity

    def __init__(self) -> None:
        self._handler = CalculateHandler.instance()

    def act(self, request: CalculateRequest):
        if not request.timestamp.isdigit():
            raise HTTPException(status_code = 403, detail = 'Invalid timestamp value')
        if request.userId is None:
            raise HTTPException(status_code = 403, detail = 'User Id can\'t be null')
        if request.apiKey is None:
            raise HTTPException(status_code = 403, detail = 'Api Key can\'t be null')
        if request.exchange is None:
            raise HTTPException(status_code = 403, detail = 'Exchange can\'t be null')
        if request.interval is None:
            raise HTTPException(status_code = 403, detail = 'Interval can\'t be null')
        if request.symbol is None:
            raise HTTPException(status_code = 403, detail = 'Symbol can\'t be null')
        if request.buyIndicator is None:
            raise HTTPException(status_code = 403, detail = 'Buy indicator can\'t be null')
        if request.sellIndicator is None:
            raise HTTPException(status_code = 403, detail = 'Sell indicator can\'t be null')
        if request.cash is None or request.cash <= 0:
            raise HTTPException(status_code = 403, detail = 'Cash must be a positive number')
        if not re.match(INDICATOR_PATTERN, request.buyIndicator):
            raise HTTPException(status_code = 403, detail = 'Invalid buy indicator')
        if not re.match(INDICATOR_PATTERN, request.sellIndicator):
            raise HTTPException(status_code = 403, detail = 'Invalid sell indicator')

        try:
            return self._handler.handle(request)
        except TestError as te:
            logging.error(f"TestError while processing /calculate", te)
            raise HTTPException(status_code = 403, detail = f'{te.message}')
        except DataProviderError as dpe:
            logging.error(f"DataProviderError while processing /calculate", dpe)
            raise HTTPException(status_code = 403, detail = f'Error while loading historical data: {dpe}')
        except NameError as ne:
            logging.error(f"NameError while processing /calculate", ne)
            raise HTTPException(status_code = 403, detail = f'Error while processing the indicator: {ne}')
        except SyntaxError as se:
            logging.error(f"SyntaxError while processing /calculate", se)
            raise HTTPException(status_code = 403, detail = f'Error while processing the indicator: {se}')
        except ValueError as ve:
            logging.error(f"ValueError while processing /calculate", ve)
            raise HTTPException(status_code = 403, detail = f'Error while processing the indicator: {ve}')
        except Exception as e:
            logging.error(f"Exception while processing /calculate", e)
            raise HTTPException(status_code = 500, detail = 'Something went wrong')

calculateActivity = CalculateActivity()