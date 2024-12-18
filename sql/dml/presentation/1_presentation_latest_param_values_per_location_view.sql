-- Creates or replaces a view named "latest_param_values_per_location" in the "presentation" schema
-- This view provides the latest air quality parameter values (e.g., PM10, PM2.5, SO2) for each location
CREATE OR REPLACE VIEW presentation.latest_param_values_per_location AS
WITH ranked_data AS (
  -- Common Table Expression (CTE) to rank rows for deduplication and filtering
  SELECT
    location_id,
    "location",
    lat,
    lon,
    "parameter",
    "value",
    "datetime",
    ROW_NUMBER() OVER (PARTITION BY location_id, "parameter" ORDER BY "datetime" DESC) AS rn
  FROM
    presentation.air_quality
)
-- Using the PIVOT operation to transform rows into columns for each air quality parameter
PIVOT (
	SELECT
		location_id,
	    "location",
	    lat,
	    lon,
	    "parameter",
	    "value",
	    "datetime"
	FROM ranked_data
	WHERE rn = 1
)
-- Pivoting on the "parameter" column to create separate columns for specific air quality parameters
ON parameter IN ('pm10', 'pm25', 'so2')
USING FIRST("value");