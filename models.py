import re
import json

from decimal import Decimal
from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class General_user(BaseModel):

    user_id: int
    username: str
    password: str
    email: str
    phone_number: str = Field(min_length=11, max_length=11)
    address: str | None
    is_cleaner: bool
    service_id_list: list[int] | None
    profile_description: str | None
    picture_url: str
    preferences: Optional[dict[str, Any]] = None 
    is_blacklist: bool = False
    blacklist_reason: str | None
    @field_validator('email')
    def enforce_email(cls, v: str):

        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        result = bool(re.match(pattern, v))

        if not result and v.count("@") > 1:

            raise Exception("Invalid input for field 'email'.")

        return v

    @field_validator('phone_number')
    def enforce_phone_number(cls, v):

        pattern = r"^\+?[1-9]\d{1,14}$"
        result = bool(re.match(pattern, v))

        if not result:

            raise Exception("Invalid input for field 'phone_number'.")

        return v

    @field_validator('preferences')
    def enforce_preferences(cls, v):

        if isinstance(v, dict):

            return json.dumps(v)

        if isinstance(v, (str, bytes, bytearray)):

            return json.loads(v)


class Service(BaseModel):

    service_id: int
    service_name: str
    by_user_id: int
    price: Decimal = Field(decimal_places=2)
    duration: str
    service_description: str
    service_tags: list[str]
    picture_url: list[str]
    listing_timestamp: datetime


class Feedback(BaseModel):

    feedback_id: int
    username: str | None
    phone_number: str | None
    feedback_text: str

class CreateFeedback(BaseModel):

    username: str | None
    phone_number: str | None
    feedback_text: str

class Payment(BaseModel):

    payment_id: int
    service_id: int
    from_user_id: int
    to_user_id: int
    price: Decimal = Field(decimal_places=2)
    payment_timestamp: datetime
    booking_timestamp: datetime

    @field_validator('payment_timestamp')
    def enforce(cls, v: datetime):

        if not v:

            raise Exception("Invalid input for field 'payment_timestamp'.")

        return v

    @field_validator('booking_timestamp')
    def enforce(cls, v: datetime):

        if not v:

            raise Exception("Invalid input for field 'booking_timestamp'.")

        return v
class InputPayment(BaseModel):
    service_id: int
    from_user_id: int
    to_user_id: int
    price: Decimal
    payment_timestamp: datetime
    booking_timestamp: datetime
class PaymentMethod(BaseModel):
    payment_method_id: int
    payment_method_name: str
    payment_method_icon: str

class PaymentReport(BaseModel):
    user_from_username: str
    user_from_user_id: int
    user_to_username: str
    user_to_user_id: int
    service_id: int
    service_tags: list[str]
    price: Decimal = Field(decimal_places=2)
    payment_timestamp: datetime
    booking_timestamp: datetime

    @field_validator('payment_timestamp')
    def enforce(cls, v: datetime):

        if not v:

            raise Exception("Invalid input for field 'payment_timestamp'.")

        return v
    @field_validator('booking_timestamp')
    def enforce(cls, v: datetime):

        if not v:

            raise Exception("Invalid input for field 'booking_timestamp'.")

        return v
    

class Review(BaseModel):

    username: str
    review_id: int
    review_score: int
    review_text: str
    by_user_id: int
    service_id: int

class ReviewReport(BaseModel):

    review_id: int
    review_score: int
    service_id: int
