import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from typing import Optional, List
from src.models.base import Base
from src.models.enumerations import StatementType
from datetime import datetime

class EntityBase(Base):
    __abstract__ = True
    id = _sql.Column(_sql.Integer, primary_key=True, index=True, autoincrement=True)
    created_at = _sql.Column(_sql.DateTime, server_default=_sql.func.now(), index=True, nullable=False)
    updated_at = _sql.Column(_sql.DateTime, server_default=_sql.func.now(), onupdate=_sql.func.now(), index=True, nullable=False)


class PersonalData(EntityBase):
    __tablename__ = "PersonalData"
    first_name = _sql.Column(_sql.String(100), index=False, nullable=False)
    last_name = _sql.Column(_sql.String(100), index=False, nullable=False)
    dob = _sql.Column(_sql.Date, index=False, nullable=False)
    phone = _sql.Column(_sql.String(15), index=False, nullable=True)
    email = _sql.Column(_sql.String(100), index=False, nullable=True)
    address = _sql.Column(_sql.String(200), index=False, nullable=True)
    pin = _sql.Column(_sql.String(10), index=False, nullable=True)
    financial_items = _orm.relationship("FinanceItem", back_populates="personal_data", cascade="all, delete-orphan")
    search_patterns = _orm.relationship("SearchPattern", back_populates="personal_data", cascade="all, delete-orphan")

    def __init__(
        self,
        first_name: str = '',
        last_name: str = '',
        dob: datetime = datetime.now(),
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
        pin: Optional[str] = None
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.phone = phone
        self.email = email
        self.address = address
        self.pin = pin

class FinanceItemCategory(EntityBase):
    __tablename__ = "FinanceItemCategory"
    name = _sql.Column(_sql.String(100), index=False, nullable=False)
    description = _sql.Column(_sql.String(200), index=False, nullable=True)
    parent_id = _sql.Column(_sql.Integer, _sql.ForeignKey("FinanceItemCategory.id"), index=True, nullable=True)
    financial_items = _orm.relationship("FinanceItem", back_populates="finance_item_category", cascade="all, delete-orphan")
    search_patterns = _orm.relationship("SearchPattern", back_populates="finance_item_category", cascade="all, delete-orphan")

    def __init__(
        self,
        name: str = '',
        description: str = '',
        parent_id: Optional[int] = None
    ):
        self.name = name
        self.description = description
        self.parent_id = parent_id

class FinanceItem(EntityBase):
    __tablename__ = "FinanceItem"
    record_date = _sql.Column(_sql.DateTime, server_default=_sql.func.now(), index=False, nullable=False)
    description = _sql.Column(_sql.String(200), index=False, nullable=False)
    finance_item_category_id = _sql.Column(_sql.Integer, _sql.ForeignKey("FinanceItemCategory.id"), index=True, nullable=False)
    finance_item_category = _orm.relationship("FinanceItemCategory", back_populates="financial_items")
    amount = _sql.Column(_sql.Float(asdecimal=True), index=True, nullable=False)
    personal_data_id = _sql.Column(_sql.Integer, _sql.ForeignKey("PersonalData.id"), index=True, nullable=False)
    personal_data = _orm.relationship("PersonalData", back_populates="financial_items")

    def __init__(
        self,
        record_date: datetime = datetime.now(),
        description: str = '',
        finance_item_category_id: int = 0,
        amount: float = 0.0,
        personal_data_id: int = 0
    ):
        self.record_date = record_date
        self.description = description
        self.amount = amount
        self.finance_item_category_id = finance_item_category_id
        self.personal_data_id = personal_data_id

class SearchPattern(EntityBase):
    __tablename__ = "SearchPattern"
    pattern = _sql.Column(_sql.String, index=False, nullable=False)
    finance_item_category_id = _sql.Column(_sql.Integer, _sql.ForeignKey("FinanceItemCategory.id"), index=True, nullable=False)
    finance_item_category = _orm.relationship("FinanceItemCategory", back_populates="search_patterns")
    personal_data_id = _sql.Column(_sql.Integer, _sql.ForeignKey("PersonalData.id"), index=True, nullable=False)
    personal_data = _orm.relationship("PersonalData", back_populates="search_patterns")

    def __init__(
            self, 
            pattern: str = '',
            finance_item_category_id: int = 0,
            personal_data_id: int = 0
        ):
        self.pattern = pattern
        self.finance_item_category_id = finance_item_category_id
        self.personal_data_id = personal_data_id

class StatementTypeSettings(EntityBase):
    __tablename__ = "StatementTypeSettings"
    statement_type = _sql.Column(_sql.Enum(StatementType), index=False, nullable=False)
    settings_json = _sql.Column(_sql.String, index=False, nullable=False)

    def __init__(
            self, 
            statement_type: StatementType = StatementType.DEFAULT,
            settings_json: str = ''):
        self.statement_type = statement_type
        self.settings_json = settings_json

class SettingsJson:
    def __init__(
            self, 
            transaction_page_keywords: List[str],
            transaction_lines_to_skip: list[str],
            description_indices: list[int] = [],
            amount_index: int = 0,
            credit_index: int = 0,
            credit_line_exists: bool = False):
        self.transaction_page_keywords = transaction_page_keywords
        self.transaction_lines_to_skip = transaction_lines_to_skip
        self.description_indices = description_indices
        self.amount_index = amount_index
        self.credit_index = credit_index
        self.credit_line_exists = credit_line_exists

    def to_json(self) -> str:
        import json
        return json.dumps({
            "transaction_page_keywords": self.transaction_page_keywords,
            "transaction_lines_to_skip": self.transaction_lines_to_skip,
            "description_indices": self.description_indices,
            "amount_index": self.amount_index,
            "credit_index": self.credit_index,
            "credit_line_exists": self.credit_line_exists
        })

    @classmethod
    def from_json(cls, json_str: str | None) -> 'SettingsJson':
        import json
        if json_str is None:
            return cls([], [])
        data = json.loads(json_str)
        return cls(
            transaction_page_keywords=data["transaction_page_keywords"],
            transaction_lines_to_skip=data["transaction_lines_to_skip"],
            description_indices=data["description_indices"],
            amount_index=data["amount_index"],
            credit_index=data["credit_index"],
            credit_line_exists=data.get("credit_line_exists", False)
        )