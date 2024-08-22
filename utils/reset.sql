DELETE FROM documentapp_signer;
DELETE FROM documentapp_document;
DELETE FROM documentapp_company;
INSERT INTO documentapp_company (name, api_token, created_at, last_updated_at)
VALUES ('ZapSign', '<API_TOKEN>', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);