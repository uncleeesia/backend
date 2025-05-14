from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class General_user(BaseModel):

    user_id: int
    username: str
    password: str
    email: str
    phone_number: str = Field(min_length=10, max_length=10)
    address: str | None
    is_cleaner: bool
    service_id_list: list[int] | None
    profile_description: str | None
    picture_url: str

    @field_validator('phone_number')
    def enforce_phone_number(cls, v):

        if "+" != v[0]:

            raise Exception("Invalid input for field 'phone_number'.")

class Service(BaseModel):

    service_id: int
    service_name: str
    by_user_id: int
    price: float = Field(decimal_places=2)
    duration: str
    service_description: str
    service_tags: list[str]
    picture_url: list[str]
        
class Feedback(BaseModel):

    feedback_id: int
    username: str
    phone_number: str = Field(min_length=10, max_length=10)
    feedback_text: str

    @field_validator('phone_number')
    def enforce_phone_number(cls, v):

        if "+" != v[0]:

            raise Exception("Invalid input for field 'phone_number'.")

class Payment(BaseModel):

    payment_id: int
    service_id: int
    from_user_id: int
    to_user_id: int
    price: float = Field(decimal_places=2)
    payment_timestamp: datetime
    booking_timestamp: datetime

    @field_validator('payment_timestamp')
    def enforce(cls, v: datetime):

        if not v:

            raise Exception("Invalid input for field 'payment_timestamp'.")
        
    @field_validator('booking_timestamp')
    def enforce(cls, v: datetime):

        if not v:

            raise Exception("Invalid input for field 'booking_timestamp'.")