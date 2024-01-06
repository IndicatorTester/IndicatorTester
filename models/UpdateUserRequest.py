from pydantic import BaseModel, Field, constr

class UpdateUserRequest(BaseModel):
    userId: constr(min_length=1, max_length=100) = Field(None)
    userData: object = Field(None)