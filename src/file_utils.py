import io
import logging
import re

from PyPDF2 import PdfReader
from fastapi import UploadFile
from typing import List
from datetime import datetime

from src.models.entities import SettingsJson
from src.models.apimodels import FinanceItemModel

def standardize_date(
        date_str: str) -> datetime:
    try:
        date_str = re.sub(r'\s+', ' ', date_str.strip())
        # Handle formats like 'DD Mon' (e.g., '12 May') or 'DD/MM/YYYY'
        for fmt in ['%d %b', '%d/%m/%Y', '%d-%m-%Y']:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                # If no year is provided, assume 2025 (based on context)
                if fmt == '%d %b':
                    parsed_date = parsed_date.replace(year=2025)
                return parsed_date
            except ValueError:
                continue
        return datetime.now()  # Default to now if no format matches
    except Exception:
        return datetime.now()

def standardize_amount(
        amount_str: str, 
        is_credit: bool=False) -> float:
    try:
        # Remove currency symbols, commas, and extra spaces
        amount_str = re.sub(r'[^\d.-]', '', amount_str)
        amount = round(float(amount_str), 2)
        # Negate amount if it's a credit (CR)
        return float(-amount if is_credit else amount)
    except:
        return 0

# Function to extract transactions from text
def extract_transactions(
        text: str,
        settings_json: SettingsJson):
    transactions: List[FinanceItemModel] = []

    amount_index = settings_json.amount_index
    credit_index = settings_json.credit_index
    credit_line_exists = settings_json.credit_line_exists

    lines = text.split('\n')
    line_index = 0
    while line_index < len(lines):
        line = lines[line_index].strip()
        date_match = re.match(r'(\d{1,2}\s+\w{3}|\d{1,2}/\d{1,2}/\d{4})', line)
        credit = False  # Default to debit
        if date_match:
            
            # Extract and standardize the date
            date_str = date_match.group(0)
            date = standardize_date(date_str)

            # Extract and standardize the description
            description_index = 1
            description = ""
            description_indices = settings_json.description_indices.copy()
            if len(description_indices) == 1:
                description_index = description_indices[0]
                description = lines[line_index + description_index].strip() if line_index + description_index < len(lines) else ''
            else:
                while description_indices:
                    description_index = description_indices.pop(0)
                    # Safely get next lines for description and amount
                    description += lines[line_index + description_index].strip() if line_index + description_index < len(lines) else ''
            if not description or any(keyword in description for keyword in settings_json.transaction_lines_to_skip):
                line_index += 1
                continue

            # Extract and standardize the amount
            amount_line = lines[line_index + amount_index].strip() if line_index + amount_index < len(lines) else ''
            if credit_line_exists:
                credit = False if lines[line_index + credit_index].strip() == 'CR' else True
            else:
                credit = True
            amount = standardize_amount(amount_line, credit)

            # Create the transaction object
            transaction = FinanceItemModel(
                record_date=date,
                description=description,
                amount=amount,
                finance_item_category_id=1,
                personal_data_id=1
            )
            transactions.append(transaction)

            if credit_line_exists and credit:
                line_index += 3
            else:
                line_index += 2
        else:
            line_index += 1
        continue
    return transactions

async def extract_transaction_pages_as_text_from_pdf(
    file: UploadFile, 
    transaction_page_keywords: list[str]
) -> str:
    """
    Extracts text from a PDF file (bytes) that contains 'Debit date', 'Description',
    and 'Amount £'. Returns the concatenated text from relevant pages.
    """
    logger = logging.getLogger(__name__)
    try:
        content: bytes = await file.read()
        reader = PdfReader(io.BytesIO(content))
        text = ""
        # transaction_page_keywords = [
        #     "Debit date",
        #     "Description",
        #     "Amount £"
        # ]
        for page in reader.pages:
            page_content = page.extract_text()
            if page_content and all(keyword in page_content for keyword in transaction_page_keywords):
                text += page_content
        return text
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}")
        raise
