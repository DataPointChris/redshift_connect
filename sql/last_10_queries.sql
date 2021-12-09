SELECT query, 
LISTAGG(CASE WHEN LEN(RTRIM(text)) = 0 THEN text 
    ELSE RTRIM(text) END) WITHIN GROUP (ORDER BY sequence) AS query_statement, 
COUNT(*) as row_count 
FROM stl_querytext
GROUP BY query
ORDER BY query desc
LIMIT 10;