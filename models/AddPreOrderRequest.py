from pydantic import BaseModel, EmailStr, Field

class AddPreOrderRequest(BaseModel):
    ip: str = Field(None)
    email: EmailStr = Field(None)