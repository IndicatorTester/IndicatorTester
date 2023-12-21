from fastapi import HTTPException
from handlers.AddPreOrderHandler import AddPreOrderHandler
from models import AddPreOrderRequest

class AddPreOrderActivity:

    @staticmethod
    def instance():
        return addPreOrderActivity

    def __init__(self):
        self._handler = AddPreOrderHandler.instance()

    def act(self, request: AddPreOrderRequest):
        try:
            self._handler.handle(request)
        except Exception as e:
            raise HTTPException(status_code = 500, detail = "Something went wrong")

addPreOrderActivity = AddPreOrderActivity()