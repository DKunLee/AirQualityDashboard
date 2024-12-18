-- Creates the "air_quality" table in the "raw" schema if it does not already exist
-- This table is designed to store raw air quality data ingested into the system
CREATE TABLE IF NOT EXISTS raw.air_quality (
	location_id BIGINT,
	sensors_id BIGINT,
	"location" VARCHAR,
	"datetime" TIMESTAMP,
	lat DOUBLE,
	lon DOUBLE,
	"parameter" VARCHAR,
	units VARCHAR,
	"value" DOUBLE,
	"month" VARCHAR,
	"year" BIGINT,
	ingestion_datetime TIMESTAMP
);