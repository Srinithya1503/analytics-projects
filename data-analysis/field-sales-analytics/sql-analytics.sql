/*
PharmaField-IQ
PostgreSQL Analytics Layer

Purpose:
Territory execution and sales effectiveness analysis

*/
-- =====================================================
-- CREATE TABLE
-- =====================================================

CREATE TABLE field_execution_data ( rep_id VARCHAR(20), rep_name VARCHAR(100), region VARCHAR(50), territory VARCHAR(50), target_value NUMERIC, 
actual_sales NUMERIC, calls_made INTEGER, samples_distributed INTEGER, achievement_percentage NUMERIC, sales_per_call NUMERIC);

-- =====================================================
-- DATA QUALITY CHECKS
-- =====================================================
-- Missing values

SELECT *

FROM field_execution_data

WHERE target_value IS NULL OR actual_sales IS NULL;

-- Duplicate representatives

SELECT rep_id, COUNT(*)
FROM field_execution_data
GROUP BY rep_id
HAVING COUNT(*) > 1;

-- =====================================================
-- TERRITORY PERFORMANCE ANALYSIS
-- =====================================================

SELECT region, territory,


COUNT(rep_id)
AS representative_count,


SUM(target_value)
AS total_target,


SUM(actual_sales)
AS total_sales,


ROUND(

SUM(actual_sales)

/

SUM(target_value)

*100,

2

)

AS achievement_percentage,


ROUND(

SUM(actual_sales)

/

SUM(calls_made),

2

)

AS sales_per_call,


AVG(samples_distributed)

AS average_samples



FROM field_execution_data



GROUP BY

region,

territory



ORDER BY

achievement_percentage;



-- =====================================================
-- UNDERPERFORMING TERRITORIES
-- =====================================================


SELECT


region,

territory,


achievement_percentage,


sales_per_call



FROM


(

SELECT


region,

territory,


ROUND(

SUM(actual_sales)

/

SUM(target_value)

*100,

2

)

AS achievement_percentage,


ROUND(

SUM(actual_sales)

/

SUM(calls_made),

2

)

AS sales_per_call



FROM field_execution_data



GROUP BY

region,

territory


)

AS performance



WHERE

achievement_percentage < 90



ORDER BY

achievement_percentage ASC;



-- =====================================================
-- REGIONAL PERFORMANCE
-- =====================================================


SELECT


region,


SUM(actual_sales)
AS regional_sales,


SUM(target_value)
AS regional_target,


ROUND(

SUM(actual_sales)

/

SUM(target_value)

*100,

2

)

AS achievement_percentage



FROM field_execution_data



GROUP BY region



ORDER BY achievement_percentage DESC;



-- =====================================================
-- FIELD PRODUCTIVITY ANALYSIS
-- =====================================================


SELECT


rep_id,

rep_name,


calls_made,


actual_sales,


ROUND(

actual_sales/calls_made,

2

)

AS sales_conversion_efficiency



FROM field_execution_data



ORDER BY

sales_conversion_efficiency DESC;

