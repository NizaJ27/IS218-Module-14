from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError, model_validator
from datetime import datetime
from typing import Optional
from app.models import CalculationType


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CalculationCreate(BaseModel):
    a: float = Field(...)
    b: float = Field(...)
    type: CalculationType = Field(...)

    @field_validator("type")
    def validate_type(cls, v):
        if not isinstance(v, CalculationType):
            # allow strings that match enum names/values
            try:
                return CalculationType(v)
            except Exception as e:
                raise ValidationError(f"Invalid calculation type: {v}") from e
        return v

    @field_validator("b")
    def validate_divisor(cls, v, info):
        # If type is Divide, b must not be zero. info is available in pydantic v2 via info
        values = info.data if hasattr(info, "data") else {}
        calc_type = values.get("type")
        if calc_type == CalculationType.DIVIDE and v == 0:
            raise ValueError("Division by zero is not allowed")
        return v

    @model_validator(mode="after")
    def check_division(cls, model):
        # cross-field validation after model is created
        try:
            calc_type = model.type
            b = model.b
        except Exception:
            return model
        if calc_type == CalculationType.DIVIDE and b == 0:
            raise ValueError("Division by zero is not allowed")
        return model


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalculationType
    result: Optional[float] = None
    user_id: Optional[int] = None

    class Config:
        orm_mode = True
