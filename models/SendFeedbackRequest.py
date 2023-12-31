from pydantic import BaseModel, EmailStr, Field, constr, validator

class SendFeedbackRequest(BaseModel):
    firstName: constr(min_length=1, max_length=50) = Field(None)
    lastName: constr(min_length=1, max_length=50) = Field(None)
    email: EmailStr = Field(None)
    message: constr(min_length=1, max_length=500) = Field(None)
    ip: str = Field(None)

    @validator("email")
    def validate_email_length(cls, value):
        if len(value) < 1 or len(value) > 50:
            raise ValueError("Email length must be between 1 and 50 characters")
        return value