import constants
from errors.TestError import TestError
from managers import TestsManager
from models import IndicatorTestRecord
from providers.CandlesProvider import CandlesProvider
from Indicators import *
from models.CalculateRequest import CalculateRequest
from utils import AwsUtils, ModelUtils

class CalculateHandler:

    @staticmethod
    def instance():
        return calculateHandler

    def __init__(self) -> None:
        self._candlesProvider = CandlesProvider.instance()
        self._awsUtils = AwsUtils.instance()
        self._testsManager = TestsManager.instance()

    def handle(self, request: CalculateRequest):
        minimumEligibleTest = self._testsManager.getMinimumEligibleTest(request.type, request.interval)

        if minimumEligibleTest is None:
            raise TestError(f"Test not found for type: [{request.type}], and interval: [{request.interval}]")

        userData = self._awsUtils.getUserData(request.userId)
        userTest = self._testsManager.getUserEligibleTest(minimumEligibleTest, userData)

        if userTest is None:
            raise TestError(f"You need test of type {minimumEligibleTest['title']} or higher to be able to run this test")

        data = self._candlesProvider.getCandles(request)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.set_index('Date').loc[request.startDate : request.endDate].reset_index()

        (date, open, high, low, close) = (
            data['Date'],
            data['Open'],
            data['High'],
            data['Low'],
            data['Close']
        )

        buyIndicatorSignals = eval(request.buyIndicator)
        sellIndicatorSignals = eval(request.sellIndicator)

        (cash, stocks, actions) = (
            request.cash,
            0,
            []
        )

        for index in range(len(buyIndicatorSignals)):
            if close[index] == 0 or buyIndicatorSignals[index] == sellIndicatorSignals[index]:
                continue
            if buyIndicatorSignals[index] and cash != 0:
                stocks = cash / close[index]
                cash = 0
                actions.append({
                    'date': str(date[index]),
                    'price': close[index],
                    'action': 'buy',
                    'stocks': stocks,
                    'cash': cash
                })
            if sellIndicatorSignals[index] and cash == 0:
                cash = stocks * close[index]
                stocks = 0
                actions.append({
                    'date': str(date[index]),
                    'price': close[index],
                    'action': 'sell',
                    'stocks': stocks,
                    'cash': cash
                })

        if cash == 0:
            cash = stocks * close[index]
            stocks = 0

        profitPercentage = round(((cash - request.cash) / request.cash) * 100.0, 2)

        if userTest["store"]:
            self._storeTestData(request, profitPercentage, actions)

        self._awsUtils.updateOrCreateDynamoItem(
            tableName=constants.AwsConstants.USERS_TABLE.value,
            primaryKey={"userId": request.userId},
            updateData={
               userTest["name"]: str(int(userData.get(userTest["name"], "0")) - 1)
            }
        )

        return {
            'start': str(date.tolist()[0]).split(' ')[0],
            'end': str(date.tolist()[-1]).split(' ')[0],
            'cash': cash,
            'actions': actions,
            'profit': cash - request.cash,
            'profitPercentage': profitPercentage,
            'success': True
        }

    def _storeTestData(self, request: CalculateRequest, profitPercentage: float, actions: []):
        indicatorTestRecord = IndicatorTestRecord(
            userId=request.userId,
            timestamp=request.timestamp,
            symbol=request.symbol,
            buyIndicator=request.buyIndicator,
            sellIndicator=request.sellIndicator,
            interval=request.interval,
            startDate=request.startDate,
            endDate=request.endDate,
            profit=str(profitPercentage)
        )
        self._awsUtils.addIndicatorTest(ModelUtils.toJson(indicatorTestRecord))
        self._awsUtils.addIndicatorTestActions(
            userId=request.userId,
            timestamp=request.timestamp,
            symbol=request.symbol,
            actions=actions
        )

calculateHandler = CalculateHandler()