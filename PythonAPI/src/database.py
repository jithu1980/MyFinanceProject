import sqlalchemy as _sql
import sqlalchemy.orm as _orm

SQLALCHEMY_DATABASE_URL = (
    "mssql+pyodbc://@2KJG544-W10\\SQLEXPRESS/MyFinanceDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
)
# Use & to separate parameters, and ensure driver name is correct and URL-encoded.

engine = _sql.create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import Base from a single source to ensure all models share the same Base
from src.models.base import Base

from src.models import entities  # Ensure all models are imported so tables are created
_ = entities  # Explicitly reference to avoid unused import warning

print(Base.metadata.tables.keys())

Base.metadata.create_all(engine)
