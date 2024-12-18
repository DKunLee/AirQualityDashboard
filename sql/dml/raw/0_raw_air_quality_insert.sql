-- Inserts data into the "raw.air_quality" table from a CSV file
INSERT INTO raw.air_quality
SELECT 
    location_id, 
    sensors_id, 
    "location", 
    "datetime", 
    lat, 
    lon, 
    "parameter", 
    units, 
    "value",
    "month", 
    "year",
    current_timestamp AS ingestion_datetime
-- Reads the data from a CSV file located at the specified file path
FROM read_csv('{{ data_file_path }}');