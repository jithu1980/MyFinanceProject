DELETE StatementTypeSettings;
DBCC CHECKIDENT ('StatementTypeSettings', RESEED, 0);

INSERT INTO StatementTypeSettings
(statement_type, settings_json)
VALUES ('SAINSBURYS_CREDIT_CARD',
        '{
            "transaction_page_keywords": [
                "Debit date",
                "Description", 
                "Amount £" ],
            "transaction_lines_to_skip": [
                "Your Direct Debit",
                "Your credit card transactions", 
                "DIRECT DEBIT RECEIVED, THANK YOU",
                "Your credit card transactions continued",
                "Debit date",
                "Description", 
                "Amount £" ],
            "description_indices": [1],
            "amount_index": 2,
            "credit_index": 3,
            "credit_line_exists": true
        }');

INSERT INTO StatementTypeSettings
(statement_type, settings_json)
VALUES ('CAPITAL_ONE_CREDIT_CARD', 
        '{
            "transaction_page_keywords": [
                "Your transaction details",
                "Paid in", 
                "Paid out" ],
            "transaction_lines_to_skip": [
                "Mr Jithu Chathukutty",
                "Your account summary",
                "Your payment details",
                "Your interest rates",
                "Going abroad?",
                "Page 2 of 2",
                "Your transaction details",
                "Paid in", 
                "Paid out",
                "Payment Received -- Thank You",
                "STATEMENT TOTALS" ],
            "description_indices": [1, 2],
            "amount_index": 4,
            "credit_index": 0,
            "credit_line_exists": false
        }');

DELETE FinanceItemCategory;
DBCC CHECKIDENT ('FinanceItemCategory', RESEED, 0);

INSERT INTO FinanceItemCategory ([name], [description], parent_id)
VALUES ('Asset', 'Parent asset category', null),
       ('Expense', 'Parent expense category', null),
       ('Income', 'Parent income category', null),
       ('Liability', 'Parent liability category', null);

INSERT INTO FinanceItemCategory ([name], [description], parent_id)
VALUES ('Amazon prime', 'Spend on Amazon prime subscription', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Broadband', 'Internet expenses', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Car', 'Purchase of car', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Asset')),
       ('Car depreciation', 'Depreciation on car', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Car insurance', 'Spend on car insurance', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Car road tax', 'Spend on road tax', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Car service & parts', 'Spend on car services and parts', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Cash at bank', 'Liquid cash at bank', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Asset')),
       ('Cinema & other tickets', 'Spend on Cinema and other tickets', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Currency', 'Currency purchases', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Asset')),
       ('Electronics', 'Spend on electronics', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Energy (Electricity & Gas)', 'Energy cost of Electricity & Gas', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Food from company', 'Spend on food from company', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Food from school', 'Spend on food from school', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Food outside', 'Spend on food from restaurant', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Food order', 'Spend on food purchases at home', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Flight', 'Spend on flight charges', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Fuel', 'Spend on fuel purchases', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Garden & Plants', 'Spend on garden & plant purchases', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Gold', 'Gold purchases', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Asset')),
       ('Grocery & Vegitables', 'Spend on Grocery & Vegitable purchases', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Gym', 'Spend on gym', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Gymnastics', 'Spend on gymnastics', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('House', 'Purchase of house', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Asset')),
       ('House apreciation', 'Apreciation on house', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Asset')),
       ('House depreciation', 'Depreciation on house', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('House hold', 'Spend on house hold purchases', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('House rent', 'Rent paid', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Hotel', 'Spend on hotel expenses', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Health insurance', 'Spend on health insurance', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Home insurance', 'Spend on home insurance', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Miscellaneous', 'Miscellaneous expenses', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Shares', 'Shares purchase', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Asset')),
       ('Shares divident', 'Income from share divident', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Short-term EMI', 'Short-term loans', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Long-term EMI', 'Long-term loans', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Liability')),
       ('Pension', 'Contribution to pension', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Asset')),
       ('Mobile', 'Spend on mobile connection', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Netflix', 'Spend on Netflix subscription', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense')),
       ('Water', 'Spend on water consumption', (SELECT id FROM FinanceItemCategory WHERE [name] = 'Expense'));
