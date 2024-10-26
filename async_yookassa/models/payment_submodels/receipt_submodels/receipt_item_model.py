import re
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field, field_validator

from async_yookassa.models.payment_submodels.amount_model import Amount
from async_yookassa.models.payment_submodels.receipt_submodels.mark_code_info_model import (
    MarkCodeInfo,
)
from async_yookassa.models.payment_submodels.receipt_submodels.mark_quantity_model import (
    MarkQuantity,
)
from async_yookassa.models.payment_submodels.receipt_submodels.payment_subject_industry_details_model import (
    PaymentSubjectIndustryDetails,
)


class ReceiptItem(BaseModel):
    description: str = Field(max_length=128)
    amount: Amount
    vat_code: int = Field(le=6)
    quantity: Decimal
    measure: str | None = None
    mark_quantity: MarkQuantity | None = None
    payment_subject: str | None = None
    payment_mode: str | None = None
    country_of_origin_code: str | None = Field(min_length=2, max_length=2, default=None)
    customs_declaration_number: str | None = Field(max_length=32, default=None)
    excise: Decimal | None = None
    product_code: str | None = None
    mark_code_info: MarkCodeInfo | None = None
    mark_mode: str | None = None
    payment_subject_industry_details: PaymentSubjectIndustryDetails | None = None

    @field_validator("quantity", mode="before")
    def quantity_validator(cls, value: Any) -> Decimal:
        """
        Устанавливает quantity модели ReceiptItem.

        :param value: quantity модели ReceiptItem.
        :type value: Decimal
        """
        return Decimal(str(float(value)))

    @field_validator("excise", mode="before")
    def excise_validator(cls, value: Any) -> Decimal:
        """ "
        Устанавливает excise модели ReceiptItem.

        :param value: excise модели ReceiptItem.
        :type value: str
        """
        return Decimal(str(value))

    @field_validator("mark_mode", mode="before")
    def mark_mode_validator(cls, value: str) -> str:
        """
        Устанавливает mark_mode модели ReceiptItem.

        :param value: mark_mode модели ReceiptItem.
        :type value: str
        """
        if not re.search(r"^0$", value):
            raise ValueError(r"Invalid value for `mark_mode`, must be a follow pattern or equal to `/^0$/`")

        return value
