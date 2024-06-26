from pydantic import BaseModel, Field
from constants import CandlesConstants

class CalculateRequest(BaseModel):
    type: str = Field(None)
    userId: str = Field(None)
    apiKey: str = Field(None)
    symbol: str = Field(None)
    exchange: str = Field(None)
    buyIndicator: str = Field(None)
    sellIndicator: str = Field(None)
    cash: float = Field(1000.0)
    timestamp: str = Field(None)
    interval: str = Field(CandlesConstants.ONE_DAY_INTERVAL.value)
    startDate: str = Field(CandlesConstants.CANDLES_ABS_START_DATE.value)
    endDate: str = Field(CandlesConstants.CANDLES_ABS_END_DATE.value)