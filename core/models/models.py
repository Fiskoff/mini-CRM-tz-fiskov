import decimal
import datetime

from sqlalchemy import Boolean, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.db_config import BaseModel


class OperatorModel(BaseModel):
    __tablename__ = "operators"

    name: Mapped[str] = mapped_column(String(256), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    max_load: Mapped[int] = mapped_column(Integer, default=10)

    distribution_rules = relationship("SourceOperatorDistribution", back_populates="operator", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="assigned_operator", cascade="all, delete-orphan")


class SourceModel(BaseModel):
    __tablename__ = "sources"

    name: Mapped[str] = mapped_column(String(256), unique=True, index=True)

    distribution_rules = relationship("SourceOperatorDistribution", back_populates="source", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="source", cascade="all, delete-orphan")


class SourceOperatorDistributionModel(BaseModel):
    __tablename__ = "source_operator_distributions"

    source_id: Mapped[int] = mapped_column(Integer, ForeignKey("sources.id"))
    operator_id: Mapped[int] = mapped_column(Integer, ForeignKey("operators.id"))
    weight: Mapped[decimal.Decimal] = mapped_column(Numeric(precision=5, scale=2), default=1.0)

    source = relationship("Source", back_populates="distribution_rules")
    operator = relationship("Operator", back_populates="distribution_rules")


class LeadModel(BaseModel):
    __tablename__ = "leads"

    external_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(13), unique=True, index=True, nullable=True)
    email: Mapped[str | None] = mapped_column(String(50), unique=True, index=True, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    contacts = relationship("Contact", back_populates="lead", cascade="all, delete-orphan")


class ContactModel(BaseModel):
    __tablename__ = "contacts"

    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("leads.id"), nullable=False)
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey("sources.id"), nullable=False)
    operator_id: Mapped[int] = mapped_column(Integer, ForeignKey("operators.id"), nullable=True)
    details: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    lead = relationship("Lead", back_populates="contacts")
    source = relationship("Source", back_populates="contacts")
    assigned_operator = relationship("Operator", back_populates="contacts")
