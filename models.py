from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class Gen_User(BaseModel):

    user_id: int
    username: str = Field(min_length=5, max_length=20)
    email: str = Field(min_length=5)
    password: str = Field(min_length=8, max_length=20)
    phone_num: str = Field(min_length=10, max_length=10)
    notification_method: int = Field(default=1)
    payment_method: int = Field(default=0)
    hidden_count: int = Field(default=0)
    removed_count: int = Field(default=0)
    favourite_list: dict | None = None
    unstruct_data: dict | None = None
    picture_url: str
        
class HomeOwner(BaseModel):

    iamsleepy: Any

class Cleaner(BaseModel):

    iwillvibecodethis: Any

class Service(BaseModel):

    service_id: int
    user_id: int
    from_date: datetime
    to_date: datetime
    view_count: int = Field(default=0)
    engagement_count: int = Field(default=0)
    category_tags: dict
    picture_url: str

    @field_validator('from_date')
    def validate_from_date(cls, v: datetime):

        if not v.tzinfo:

            raise Exception("Invalid value for field 'from_date'.")
        
    @field_validator('to_date')
    def validate_from_date(cls, v: datetime):

        if not v.tzinfo:

            raise Exception("Invalid value for field 'to_date'.")
        
class Feedback(BaseModel):

    feedback_id: int
    by_user_id: int
    from_user_id: int
    service_id: int
    rating: int = Field(ge=0, le=10)
    feedback_text: dict
    is_hidden: bool
    is_removed: bool

class Payment(BaseModel):

    payment_id: int
    payment_method: int = Field(default=0)
    service_id: int
    from_user_id: int
    by_user_id: int
    is_completed: bool
    payment_timestamp: datetime

    @field_validator('payment_timestamp')
    def validate_payment_timestamp(cls, v: datetime):

        if not v.tzinfo:

            raise Exception("Invalid value for field 'payment_timestamp'.")