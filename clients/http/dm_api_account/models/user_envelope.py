from __future__ import annotations
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, \
    ConfigDict, \
    Field

from typing import List, \
    Optional, \
    Dict


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Player"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class User(BaseModel):
    login: str
    roles: List[UserRole] = Field(None)
    medium_picture_url: str = Field(None, alias="mediumPictureUrl")
    small_picture_url: str = Field(None, alias="smallPictureUrl")
    status: str = Field(None)
    rating: Rating
    online: datetime = Field(None)
    name: str = Field(None)
    location: str = Field(None)
    registration: datetime = Field(None)


class UserEnvelope(BaseModel):
    model_config = ConfigDict(extra='forbid')
    resource: Optional[User] = None
    metadata: Optional[Dict[str, str]] = None
