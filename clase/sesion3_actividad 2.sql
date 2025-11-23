CREATE OR REPLACE FUNCTION calcular_gc_porcentaje(secuencia_adn TEXT)
RETURNS NUMERIC(5,2)
LANGUAGE plpgsql
AS $$
DECLARE
    total_bases INTEGER;
    cantidad_g INTEGER;
    cantidad_c INTEGER;
    gc_contenido NUMERIC(5,2);
BEGIN
    -- Contar el total de bases
    total_bases := LENGTH(secuencia_adn);
    
    -- Contar Guaninas (G)
    cantidad_g := LENGTH(secuencia_adn) - LENGTH(REPLACE(UPPER(secuencia_adn), 'G', ''));
    
    -- Contar Citosinas (C)
    cantidad_c := LENGTH(secuencia_adn) - LENGTH(REPLACE(UPPER(secuencia_adn), 'C', ''));
    
    -- Calcular porcentaje GC
    IF total_bases > 0 THEN
        gc_contenido := ((cantidad_g + cantidad_c)::NUMERIC / total_bases) * 100;
    ELSE
        gc_contenido := 0;
    END IF;
    
    RETURN ROUND(gc_contenido, 2);
END;
$$;

CREATE OR REPLACE FUNCTION clasificar_gc(gc_porcentaje NUMERIC)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
BEGIN
    IF gc_porcentaje < 30 THEN
        RETURN 'Bajo GC (<30%)';
    ELSIF gc_porcentaje >= 30 AND gc_porcentaje < 40 THEN
        RETURN 'Medio-Bajo GC (30-40%)';
    ELSIF gc_porcentaje >= 40 AND gc_porcentaje < 50 THEN
        RETURN 'Medio GC (40-50%)';
    ELSIF gc_porcentaje >= 50 AND gc_porcentaje < 60 THEN
        RETURN 'Medio-Alto GC (50-60%)';
    ELSE
        RETURN 'Alto GC (≥60%)';
    END IF;
END;
$$;

SELECT 
    s.accession_number,
    calcular_gc_porcentaje(s.secuencia) AS gc_calculado,
    c.porcentaje_gc AS gc_almacenado,
    ABS(calcular_gc_porcentaje(s.secuencia) - c.porcentaje_gc) AS diferencia,
    clasificar_gc(c.porcentaje_gc) AS clasificacion
FROM secuencia s
LEFT JOIN composicion_nucleotidos c ON s.id_secuencia = c.id_secuencia
ORDER BY s.accession_number;