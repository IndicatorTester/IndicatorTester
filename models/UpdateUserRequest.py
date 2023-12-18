from pydantic import BaseModel, Field

class UpdateUserRequest(BaseModel):
    userId: str = Field(None)
    userData: object = Field(None)