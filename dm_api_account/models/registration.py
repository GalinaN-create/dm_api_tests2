from pydantic import BaseModel, \
    Field, \
    ConfigDict


class Registration(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description='Логин')
    email: str = Field(..., description='Почта')
    password: str = Field(..., description='Пароль')
