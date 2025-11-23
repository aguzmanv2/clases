CREATE OR REPLACE FUNCTION validar_longitud_secuencia()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar que la longitud sea mayor o igual a 100
    IF NEW.longitud < 100 THEN
        RAISE EXCEPTION 'Error: La secuencia % tiene solo % bases. Se requieren al menos 100 bases.',
            NEW.accession_number,
            NEW.longitud
        USING HINT = 'Las secuencias deben tener un mínimo de 100 nucleótidos para garantizar análisis significativos.';
    END IF;
    
    -- Verificar que la longitud declarada coincida con la secuencia real
    IF LENGTH(NEW.secuencia) < 100 THEN
        RAISE EXCEPTION 'Error: La secuencia real de % tiene solo % caracteres. Se requieren al menos 100.',
            NEW.accession_number,
            LENGTH(NEW.secuencia)
        USING HINT = 'Verifique que la secuencia de ADN sea completa.';
    END IF;
    
    -- Verificar que longitud declarada coincida con longitud real
    IF NEW.longitud != LENGTH(NEW.secuencia) THEN
        RAISE WARNING 'Advertencia: La longitud declarada (%) no coincide con la longitud real (%) para %',
            NEW.longitud,
            LENGTH(NEW.secuencia),
            NEW.accession_number;
        -- Corregir automáticamente
        NEW.longitud := LENGTH(NEW.secuencia);
    END IF;
    
    -- Si todo está correcto, permitir la inserción
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trigger_validar_insert_secuencia ON secuencia;

CREATE TRIGGER trigger_validar_insert_secuencia
    BEFORE INSERT ON secuencia
    FOR EACH ROW
    EXECUTE FUNCTION validar_longitud_secuencia();

DROP TRIGGER IF EXISTS trigger_validar_update_secuencia ON secuencia;

CREATE TRIGGER trigger_validar_update_secuencia
    BEFORE UPDATE ON secuencia
    FOR EACH ROW
    WHEN (OLD.secuencia IS DISTINCT FROM NEW.secuencia OR 
          OLD.longitud IS DISTINCT FROM NEW.longitud)
    EXECUTE FUNCTION validar_longitud_secuencia();