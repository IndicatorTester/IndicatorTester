from pydantic import BaseModel, Field
from constants import CandlesConstants

class CalculateExchangeRequest(BaseModel):
    exchange: str = Field(None)
    indicator: str = Field(None)
    cash: float = Field(1000.0)
    interval: str = Field(CandlesConstants.ONE_DAY_INTERVAL.value)
    startDate: str = Field(CandlesConstants.CANDLES_ABS_START_DATE.value)
    endDate: str = Field(CandlesConstants.CANDLES_ABS_END_DATE.value)