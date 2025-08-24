import src.database as _database
import logging

from src.models.entities import EntityBase, StatementTypeSettings, SettingsJson
from src.models.enumerations import StatementType
from sqlalchemy.orm import Session
from sqlalchemy import func

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console
        logging.FileHandler('app.log', encoding='utf-8')  # File
    ]
)
logger = logging.getLogger(__name__)

# Dependency to get DB session
def get_database_session():
    logger.info("Creating new database session.")
    database_session = _database.SessionLocal()
    try:
        yield database_session
    finally:
        logger.info("Closing database session.")
        database_session.close()

# Utility function to add models to the database
def add_models_to_database(entity: EntityBase, database_session: Session):
    logger.info(f"Adding entity to database: {entity}")
    try:
        database_session.add(entity)
        database_session.commit()
        database_session.refresh(entity)
        logger.info("Entity added and committed successfully.")
    except Exception as e:
        logger.error(f"Error adding entity to database: {e}")
        database_session.rollback()
        raise

async def add_or_update_model(entity: EntityBase, database_session: Session) -> EntityBase:
    logger.info(f"Adding or updating entity in database: {entity}")
    try:
        if hasattr(entity, "id") and isinstance(getattr(entity, "id", None), int) and getattr(entity, "id", 0) > 0:
            db_entity = database_session.get(type(entity), entity.id)
            if db_entity:
                for attr, value in entity.__dict__.items():
                    if attr != '_sa_instance_state':
                        setattr(db_entity, attr, value)
                database_session.commit()
                database_session.refresh(db_entity)
                logger.info("Entity updated successfully.")
                return db_entity
        database_session.add(entity)
        database_session.commit()
        database_session.refresh(entity)
        logger.info("Entity added successfully.")
    
        return entity
    
    except Exception as e:
        logger.error(f"Error adding or updating entity: {e}")
        database_session.rollback()
        raise

def get_all_statement_type_settings(database_session: Session) -> list[StatementTypeSettings]:
    """Fetch all StatementTypeSettings records from the database."""

    return database_session.query(StatementTypeSettings).all()

def get_statement_type_settings_by_type(
    database_session: Session, statement_type: StatementType
) -> SettingsJson:
    """Fetch the settings_json from StatementTypeSettings by statement_type."""

    query = database_session.query(StatementTypeSettings)
    if statement_type:
        query = query.filter(
            func.lower(StatementTypeSettings.statement_type).__eq__(f"{statement_type.value.lower()}")  # type: ignore
        )
    statement_type_settings = query.first()
    
    if statement_type_settings is not None and getattr(statement_type_settings, "settings_json", "") != "":
        settings_json_str = str(statement_type_settings.settings_json)
        settings = SettingsJson.from_json(settings_json_str)
        return settings
    else:
        return SettingsJson([], [])  # Default empty settings
