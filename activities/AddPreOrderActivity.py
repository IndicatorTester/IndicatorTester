from fastapi import HTTPException
from handlers.AddPreOrderHandler import AddPreOrderHandler
from models import AddPreOrderRequest
import logging

class AddPreOrderActivity:

    @staticmethod
    def instance():
        return addPreOrderActivity

    def __init__(self):
        self._handler = AddPreOrderHandler.instance()

    def act(self, request: AddPreOrderRequest):
        logging.info(f"Handle add per order with email: [{request.email}], and ip: [{request.ip}]")
        if request.ip is None:
            raise HTTPException(status_code = 403, detail = 'IP address can\'t be null')
        if request.email is None:
            raise HTTPException(status_code = 403, detail = 'Email can\'t be null')

        try:
            self._handler.handle(request)
        except Exception as e:
            logging.error(f"Exception while adding per order for email: [{request.email}], error: {e}")
            raise HTTPException(status_code = 500, detail = "Something went wrong")

addPreOrderActivity = AddPreOrderActivity()