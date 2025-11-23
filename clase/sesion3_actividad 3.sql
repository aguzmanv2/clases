CREATE OR REPLACE VIEW comparacion_gc AS
SELECT 
    e.id_especie,
    e.nombre_cientifico,
    e.nombre_comun,
    s.id_secuencia,
    s.accession_number,
    s.tipo_secuencia,
    s.longitud,
    c.porcentaje_gc,
    clasificar_gc(c.porcentaje_gc) AS clasificacion_gc,
    c.cantidad_g,
    c.cantidad_c,
    c.cantidad_a,
    c.cantidad_t
FROM especie e
JOIN secuencia s ON e.id_especie = s.id_especie
LEFT JOIN composicion_nucleotidos c ON s.id_secuencia = c.id_secuencia
ORDER BY e.nombre_cientifico, s.accession_number;

SELECT 
    nombre_cientifico,
    accession_number AS id_secuencia,
    tipo_secuencia,
    longitud,
    porcentaje_gc AS "GC%",
    clasificacion_gc
FROM comparacion_gc
ORDER BY nombre_cientifico, accession_number;

CREATE OR REPLACE VIEW estadisticas_gc_por_especie AS
SELECT 
    nombre_cientifico,
    nombre_comun,
    COUNT(id_secuencia) AS total_secuencias,
    ROUND(AVG(porcentaje_gc), 2) AS gc_promedio,
    MIN(porcentaje_gc) AS gc_minimo,
    MAX(porcentaje_gc) AS gc_maximo,
    ROUND(STDDEV(porcentaje_gc), 2) AS gc_desviacion_std,
    ROUND(AVG(longitud), 0) AS longitud_promedio
FROM comparacion_gc
WHERE porcentaje_gc IS NOT NULL
GROUP BY nombre_cientifico, nombre_comun
ORDER BY gc_promedio DESC;


