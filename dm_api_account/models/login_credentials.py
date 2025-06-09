from pydantic import BaseModel, \
    ConfigDict, \
    Field


class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description='Логин')
    password: str = Field(..., description='Пароль')
    remember_me: bool = Field(..., description='Пароль', serialization_alias='rememberMe')
