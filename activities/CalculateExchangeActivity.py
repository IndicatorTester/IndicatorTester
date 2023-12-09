from handlers.CalculateExchangeHandler import CalculateExchangeHandler
from models import CalculateExchangeRequest

class CalculateExchangeActivity:

    @staticmethod
    def instance():
        return calculateExchangeActivity

    def __init__(self, calculateExchangeHandler: CalculateExchangeHandler) -> None:
        self._handler = calculateExchangeHandler

    def act(self, request: CalculateExchangeRequest):
        return self._handler.handle(request)

calculateExchangeActivity = CalculateExchangeActivity(CalculateExchangeHandler.instance())