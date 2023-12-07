from handlers.GetSymbolsHandler import GetSymbolsHandler

class GetSymbolsActivity:

    @staticmethod
    def instance():
        return getSymbolsActivity

    def __init__(self, handler: GetSymbolsHandler) -> None:
        self._handler = handler
    
    def act(self):
        return self._handler.handle();

getSymbolsActivity = GetSymbolsActivity(GetSymbolsHandler.instance())