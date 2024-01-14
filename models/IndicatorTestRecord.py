from pydantic import BaseModel, Field

class IndicatorTestRecord(BaseModel):
    userId: str = Field(None)
    timestamp: str = Field(None)
    symbol: str = Field(None)
    buyIndicator: str = Field(None)
    sellIndicator: str = Field(None)
    interval: str = Field(None)
    startDate: str = Field(None)
    endDate: str = Field(None)
    profit: str = Field(None)