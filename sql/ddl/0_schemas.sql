-- Creates the "raw" schema if it does not already exist
-- The "raw" schema is typically used to store raw or unprocessed data, directly ingested from the source
CREATE SCHEMA IF NOT EXISTS "raw";

-- Creates the "presentation" schema if it does not already exist
-- The "presentation" schema is commonly used to store processed or transformed data,
-- often prepared for reporting, visualization, or end-user consumption
CREATE SCHEMA IF NOT EXISTS "presentation";
