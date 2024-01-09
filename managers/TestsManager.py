from utils import AwsUtils

TESTS = [
    {
        "title": "Bronze",
        "name": "bronzeTest",
        "types": ["stocks"],
        "intervals": ["1day", "1week", "1month"],
        "level": 1,
        "store": False
    },
    {
        "title": "Silver",
        "name": "silverTest",
        "types": ["stocks"],
        "intervals": ["1min", "5min", "15min", "30min", "45min", "1h", "2h", "4h", "1day", "1week", "1month"],
        "level": 2,
        "store": False
    },
    {
        "title": "Gold",
        "name": "goldTest",
        "types": ["stocks", "cryptocurrencies"],
        "intervals": ["1day", "1week", "1month"],
        "level": 3,
        "store": True
    },
    {
        "title": "Diamond",
        "name": "diamondTest",
        "types": ["stocks", "cryptocurrencies"],
        "intervals": ["1min", "5min", "15min", "30min", "45min", "1h", "2h", "4h", "1day", "1week", "1month"],
        "level": 4,
        "store": True
    },
]

class TestsManager:

    @staticmethod
    def instance():
        return testsManager

    def __init__(self) -> None:
        self._awsUtils = AwsUtils.instance()

    def getMinimumEligibleTest(self, type, interval):
        for test in TESTS:
            if type in test["types"] and interval in test["intervals"]:
                return test
        return None

    def getUserEligibleTest(self, minimumEligibleTest, userData):
        print(userData)
        for test in TESTS:
            if int(userData.get(test["name"], 0)) > 1 and test["level"] >= minimumEligibleTest["level"]:
                return test
        return None

testsManager = TestsManager()