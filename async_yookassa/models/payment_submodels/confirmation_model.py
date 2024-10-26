from enum import Enum

from pydantic import BaseModel, model_validator


class TypeEnum(str, Enum):
    embedded = "embedded"
    external = "external"
    mobile_application = "mobile_application"
    qr = "qr"
    redirect = "redirect"


class Confirmation(BaseModel):
    type: TypeEnum
    locale: str | None = None
    return_url: str | None = None
    enforce: bool | None = None

    class Config:
        use_enum_values = True

    @model_validator(mode="before")
    def validate_required_fields(cls, values):
        type_value = values.get("type")

        if type_value == TypeEnum.mobile_application:
            if not values.get("return_url"):
                raise ValueError("Field 'return_url' is required for type 'mobile_application'")

        if type_value == TypeEnum.redirect:
            if not values.get("return_url"):
                raise ValueError("Field 'return_url' is required for type 'redirect'")
