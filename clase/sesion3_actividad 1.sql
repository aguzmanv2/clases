SELECT 
    s.id_secuencia,
    e.nombre_cientifico,
    s.accession_number,
    s.tipo_secuencia,
    s.longitud AS longitud_nucleotidos,
    TO_CHAR(s.longitud, '999,999,999') AS longitud_formateada
FROM secuencia s
JOIN especie e ON s.id_especie = e.id_especie
ORDER BY s.longitud DESC;

SELECT 
    e.nombre_cientifico,
    e.nombre_comun,
    COUNT(s.id_secuencia) AS total_secuencias,
    MIN(s.longitud) AS longitud_minima,
    MAX(s.longitud) AS longitud_maxima,
    ROUND(AVG(s.longitud), 2) AS longitud_promedio,
    MAX(s.longitud) - MIN(s.longitud) AS diferencia_max_min,
    ROUND(STDDEV(s.longitud), 2) AS desviacion_estandar
FROM especie e
JOIN secuencia s ON e.id_especie = s.id_especie
GROUP BY e.id_especie, e.nombre_cientifico, e.nombre_comun
ORDER BY longitud_promedio DESC;

SELECT 
    e.nombre_cientifico,
    s.accession_number,
    s.longitud,
    ROUND(AVG(s.longitud) OVER (), 2) AS promedio_general,
    s.longitud - ROUND(AVG(s.longitud) OVER (), 2) AS diferencia_del_promedio
FROM secuencia s
JOIN especie e ON s.id_especie = e.id_especie
WHERE s.longitud > (SELECT AVG(longitud) FROM secuencia)
ORDER BY diferencia_del_promedio DESC;

SELECT 
    RANK() OVER (ORDER BY s.longitud DESC) AS ranking,
    e.nombre_cientifico,
    s.accession_number,
    s.tipo_secuencia,
    s.longitud,
    ROUND((s.longitud::NUMERIC / SUM(s.longitud) OVER ()) * 100, 2) AS porcentaje_del_total
FROM secuencia s
JOIN especie e ON s.id_especie = e.id_especie
ORDER BY ranking;