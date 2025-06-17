from __future__ import annotations
from datetime import datetime

from enum import Enum

from pydantic import BaseModel, \
    ConfigDict, \
    Field

from typing import List, \
    Optional, \
    Union


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class ParseMode(str, Enum):
    COMMON = "Common"
    INFO = "Info"
    POST = "Post"
    CHAT = "Chat"


class InfoBbText(BaseModel):
    value: str
    parse_mode: ParseMode = Field(alias="parseMode")


class PagingSettings(BaseModel):
    posts_per_page: int = Field(None, alias="postsPerPage")
    comments_per_page: int = Field(None, alias="commentsPerPage")
    topics_per_page: int = Field(None, alias="topicsPerPage")
    messages_per_page: int = Field(None, alias="messagesPerPage")
    entities_per_page: int = Field(None, alias="entitiesPerPage")


class ColorSchema(str, Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSIC_PALE = "ClassicPale"
    NIGHT = "Night"


class UserSettings(BaseModel):
    color_schema: ColorSchema = Field(None, alias="colorSchema")
    nanny_greetings_message: str = Field(None, alias="nannyGreetingsMessage")
    paging: PagingSettings


class UserRole(str, Enum):
    # [ Guest, Player, Administrator, NannyModerator, RegularModerator, SeniorModerator ]
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Player"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class UserDetails(BaseModel):
    login: str
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias="mediumPictureUrl")
    small_picture_url: str = Field(None, alias="smallPictureUrl")
    status: str = Field(None)
    rating: Rating
    online: datetime
    name: str = Field(None)
    location: str = Field(None)
    registration: datetime
    icq: str = Field(None)
    skype: str = Field(None)
    original_picture_url: str = Field(None, alias="originalPictureUrl")
    info: Union[InfoBbText, str, None] = Field(None)
    settings: UserSettings


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra='forbid')
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None
