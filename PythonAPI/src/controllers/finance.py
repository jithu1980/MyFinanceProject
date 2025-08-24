#--------------------------------------------------------------------------------------------
# Third library party imports
#--------------------------------------------------------------------------------------------
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi import Body, Depends
from sqlalchemy.orm import Session
from typing import Any
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import logging
from datetime import datetime
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Custom library imports
#--------------------------------------------------------------------------------------------
from src.models.apimodels import FinanceItemCategoryModel, FinanceItemModel, PersonalDataModel
from src.models.entities import PersonalData, FinanceItemCategory, FinanceItem, SettingsJson
from src.models.enumerations import StatementType
from src.file_utils import extract_transaction_pages_as_text_from_pdf, extract_transactions
from src.entitybuilder import add_or_update_model, get_database_session, get_statement_type_settings_by_type
from src.extensions.object_extensions import to_json
#--------------------------------------------------------------------------------------------

app = FastAPI()

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


@app.get("/ping")
async def ping() -> dict[str, Any]:
    return {
        "message": "pong", 
        "timestamp": datetime.now().isoformat()}


#--------------------------------------------------------------------------------------------
# POST: Create Personal Data
#--------------------------------------------------------------------------------------------
@app.post("/personal-data/")
async def create_personal_data(
    personal_data_model: PersonalDataModel = Body(...),
    database_session: Session = Depends(get_database_session)
) -> str:
    logger.info(f"Creating PersonalData: {personal_data_model}")
    personal_data = PersonalData(
        first_name=personal_data_model.first_name,
        last_name=personal_data_model.last_name,
        dob=personal_data_model.dob,
        phone=personal_data_model.phone,
        email=personal_data_model.email,
        address=personal_data_model.address,
        pin=personal_data_model.pin
    )
    personal_data = await add_or_update_model(personal_data, database_session)
    logger.info("PersonalData saved successfully.")

    return to_json(personal_data)  # Using utility function

#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# POST: Upload PDF and extract transactions
#--------------------------------------------------------------------------------------------
@app.post("/upload-pdf/")
async def upload_pdf(
    pdf_file: UploadFile = File(...),
    statement_type: StatementType = Body(...),
    database_session: Session = Depends(get_database_session)
) -> list[FinanceItemModel]:
    logger.info(f"Received file upload: {pdf_file.filename}")
    try:
        settings_json_obj: SettingsJson = get_statement_type_settings_by_type(
            database_session,
            statement_type)

        pdf_content = await extract_transaction_pages_as_text_from_pdf(
            pdf_file, 
            settings_json_obj.transaction_page_keywords)

        extracted_transactions: list[FinanceItemModel] = extract_transactions(
            pdf_content, 
            settings_json_obj
        )        # file_path = await save_pdf_file(pdf_file)

        # Convert FinanceItem objects to dicts for FastAPI serialization
        return extracted_transactions
        
    except Exception as e:
        logger.error(f"Failed to read PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to read PDF: {str(e)}")
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# POST: Create Finance Item Category
#--------------------------------------------------------------------------------------------
@app.post("/finance-item-category/")
async def create_finance_item_category(
    finance_item_category_model: FinanceItemCategoryModel = Body(...),
    database_session: Session = Depends(get_database_session)
) -> str:
    logger.info(f"Creating FinanceItemCategory: {finance_item_category_model}")
    finance_item_category = FinanceItemCategory(
        name=finance_item_category_model.name,
        description=finance_item_category_model.description
    )
    finance_item_category = await add_or_update_model(finance_item_category, database_session)
    logger.info("FinanceItemCategory saved successfully.")

    return to_json(finance_item_category)  # Using utility function

#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# POST: Create Finance Item
#--------------------------------------------------------------------------------------------
@app.post("/finance-item/")
async def create_finance_item(
    finance_item_model: FinanceItemModel = Body(...),
    database_session: Session = Depends(get_database_session)
) -> str:
    logger.info(f"Creating FinanceItem: {finance_item_model}")
    finance_item = FinanceItem(
        record_date=finance_item_model.record_date,
        description=finance_item_model.description,
        finance_item_category_id=finance_item_model.finance_item_category_id,
        amount=finance_item_model.amount,
        personal_data_id=finance_item_model.personal_data_id
    )
    finance_item = await add_or_update_model(finance_item, database_session)
    logger.info("FinanceItem saved successfully.")

    return to_json(finance_item)  # Using utility function

#--------------------------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )
#--------------------------------------------------------------------------------------------
