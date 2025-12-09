import datetime
from typing import Optional, List

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class OperatorBaseSchema(BaseModel):
    name: str
    is_active: bool = True
    max_load: int = 10


class OperatorCreateSchema(OperatorBaseSchema):
    pass


class OperatorUpdateSchema(BaseModel):
    is_active: Optional[bool] = None
    max_load: Optional[int] = None


class OperatorSchema(OperatorBaseSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SourceBaseSchema(BaseModel):
    name: str


class SourceCreateSchema(SourceBaseSchema):
    pass


class SourceSchema(SourceBaseSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class DistributionSettingBaseSchema(BaseModel):
    source_id: int
    operator_id: int
    weight: float = 1.0


class DistributionSettingCreateSchema(DistributionSettingBaseSchema):
    pass


class DistributionSettingUpdateSchema(BaseModel):
    weight: Optional[float] = None


class DistributionSettingSchema(DistributionSettingBaseSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class LeadBaseSchema(BaseModel):
    external_id: str
    phone: Optional[str] = None
    email: Optional[str] = None


class LeadCreateSchema(LeadBaseSchema):
    pass


class LeadSchema(LeadBaseSchema):
    id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    model_config = ConfigDict(from_attributes=True)


class ContactRegisterRequestSchema(BaseModel):
    lead_identifier: str = Field(..., description="Может быть внешним идентификатором, телефоном или почтой")
    source_name: str
    details: Optional[str] = None


class ContactRegisterResponseSchema(BaseModel):
    contact_id: int
    lead_id: int
    source_id: int
    assigned_operator: Optional[OperatorSchema] = None
    message: str


class LeadWithContactsSchema(LeadSchema):
    contacts: List['ContactViewSchema'] = []


class ContactViewSchema(BaseModel):
    id: int
    source_name: str
    operator_name: Optional[str]
    created_at: datetime.datetime
    is_active: bool
    details: Optional[str]

    model_config = ConfigDict(from_attributes=True)