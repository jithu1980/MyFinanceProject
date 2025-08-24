from pydantic import BaseModel
from datetime import datetime

class FinanceItemCategoryModel(BaseModel):
    name: str
    description: str

class FinanceItemModel(BaseModel):
    record_date: datetime
    description: str
    amount: float
    finance_item_category_id: int
    personal_data_id: int

class PersonalDataModel(BaseModel):
    first_name: str
    last_name: str
    dob: datetime
    phone: str
    email: str
    address: str
    pin: str