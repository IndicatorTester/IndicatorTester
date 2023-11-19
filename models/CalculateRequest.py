from pydantic import BaseModel, Field

class CalculateRequest(BaseModel):
    symbol: str = Field(None)
    indicator: str = Field(None)
    cash: float = Field(1000.0)
    startDate: str = Field('2000-01-01')
    endDate: str = Field('2029-12-31')