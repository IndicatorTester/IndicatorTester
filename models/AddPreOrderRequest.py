from pydantic import BaseModel, Field

class AddPreOrderRequest(BaseModel):
    ip: str = Field(None)
    email: str = Field(None)