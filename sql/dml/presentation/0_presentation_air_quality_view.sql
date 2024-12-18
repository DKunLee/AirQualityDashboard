-- Creates or replaces a view named "air_quality" in the "presentation" schema
-- This view provides deduplicated and filtered air quality data from the raw.air_quality table
CREATE OR REPLACE VIEW presentation.air_quality AS (
    -- Temporary CTE (Common Table Expression) to rank data for deduplication
    WITH ranked_data AS (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY location_id, sensors_id, "datetime", "parameter"
                ORDER BY ingestion_datetime DESC
            ) AS rn
            -- Assigns a row number to each record based on the latest ingestion timestamp
            -- for each combination of location_id, sensors_id, datetime, and parameter
        FROM raw.air_quality
        WHERE parameter IN ('pm10', 'pm25', 'so2')
        AND "value" >= 0
    )
    -- Final query selecting only the top-ranked (latest) record for each partition
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
        ingestion_datetime
    FROM ranked_data
    WHERE rn = 1
);