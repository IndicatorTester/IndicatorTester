import requests
import json
import hashlib
import hmac
import time
from datetime import datetime
import logging
from decimal import Decimal, ROUND_DOWN
from utils import AwsUtils

API_KEY = 'JBPv6OAXcOocfQHZcP'
API_SECRET = 'iSfixmKOHeDFMbfc3iyJ8Rhvn6heK7ktpkDw'

class BybitUtils:

    @staticmethod
    def instance():
        return bybitUtils

    def __init__(self) -> None:
        self._awsUtils = AwsUtils.instance()

    def trade(self, symbol: str, signal: str):
        try :
            logging.info(f"Starting a trade for symbol: {symbol}, with signal: {signal}")
            currentUSDT = self._getSpotCoin("USDT")['result']['spot']['assets'][0]['free']
            time.sleep(5)

            url = 'https://api.bybit.com/v5/order/create/?'
            timestamp = int(datetime.utcnow().timestamp()) * 1000
            # timestamp = int(datetime.utcnow().timestamp()) * 1000 + (3 * 60 * 60 * 1000)
            recvWindow = 5000

            baseCoin, quoteCoin = symbol.split('/')[0], "USDT"
            coinData = self._getSpotCoin(baseCoin)

            if coinData is None:
                return "Unable to get coin data from ByBit"

            freeAmount = coinData['result']['spot']['assets'][0]['free']
            coinQty = Decimal(freeAmount).quantize(Decimal('0.0'), rounding=ROUND_DOWN)
            usdtQty = self._awsUtils.getByBitCoinAsset(baseCoin)

            body = {
                "category": "spot",
                "symbol": baseCoin + quoteCoin,
                "side": signal,
                "orderType": "Market",
                "qty": str(usdtQty) if signal == "Buy" else str(coinQty),
                "baseCoin": baseCoin,
                "quoteCoin": quoteCoin
            }

            logging.info(f"Action {signal} on {symbol} with quantity: {body['qty']}")

            headers = {
                'Content-Type': 'application/json',
                'X-BAPI-SIGN': self._generateSign(json.dumps(body), timestamp, recvWindow),
                'X-BAPI-API-KEY': API_KEY,
                "X-BAPI-RECV-WINDOW": str(recvWindow),
                'X-BAPI-TIMESTAMP': str(timestamp),
            }

            response = requests.post(url, headers=headers, json=body).json()
            # response = {'retCode': 0}
            if response['retCode'] == 0:
                time.sleep(10)
                if signal == 'Sell':
                    newUSDT = self._getSpotCoin("USDT")['result']['spot']['assets'][0]['free']
                    newAssetValue = str(
                        Decimal(newUSDT).quantize(Decimal('0.0'), rounding=ROUND_DOWN) - Decimal(currentUSDT).quantize(Decimal('0.0'), rounding=ROUND_DOWN)
                    )
                    self._awsUtils.updateByBitCoinAsset(
                        baseCoin,
                        newAssetValue
                    )
                    return f"Sell Trade succeeded with and the asset value became: {newAssetValue}"
                else:
                    self._awsUtils.updateByBitCoinAsset(
                        baseCoin,
                        "0.0"
                    )
                    return "Buy Trade succeeded"

            logging.warn(f"Unable to trade with Bybit with response: {json.dumps(response)}")
            return f"Unable to trade with Bybit with response: {json.dumps(response)}"
        except Exception as e:
            logging.error(f"An error occurred while Trading with Bybit: {str(e)}", e)
            return f"An error occurred while Trading with Bybit: {str(e)}"

    def _getSpotCoin(self, coin: str):
        try :
            url = f'https://api.bybit.com/v5/asset/transfer/query-asset-info/?accountType=SPOT&coin={coin}'
            timestamp = int(datetime.utcnow().timestamp()) * 1000
            # timestamp = int(datetime.utcnow().timestamp()) * 1000 + (3 * 60 * 60 * 1000)
            recvWindow = 5000

            headers = {
                'Content-Type': 'application/json',
                'X-BAPI-SIGN': self._generateSign(f'accountType=SPOT&coin={coin}', timestamp, recvWindow),
                'X-BAPI-API-KEY': API_KEY,
                "X-BAPI-RECV-WINDOW": str(recvWindow),
                'X-BAPI-TIMESTAMP': str(timestamp)
            }

            response = requests.get(url, headers=headers).json()
            if response['retCode'] == 0:
                return response

            logging.warn(f"Unable to trade with Bybit with response: {response}")
            return None
        except Exception as e:
            logging.error(f"An error occurred while getting Spot Assets with Bybit: {str(e)}", e)
            return None

    def _generateSign(self, sign_request_params, timestamp, recv_window):
        params_str = str(timestamp) + API_KEY + str(recv_window) + sign_request_params
        signature = hmac.new(bytes(API_SECRET, 'utf-8'), bytes(params_str, 'utf-8'), hashlib.sha256).hexdigest()
        return signature

bybitUtils = BybitUtils()