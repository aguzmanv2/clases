import csv
import sys
import psycopg2
import os

# Aumentar límite de campo CSV (compatible con Windows)
try:
    csv.field_size_limit(sys.maxsize)
except OverflowError:
    # En Windows, usar un valor más pequeño pero suficiente
    csv.field_size_limit(2147483647)  # 2^31 - 1


def conectar_postgres(host='localhost', database='genetica_comparada', 
                     user='postgres', password='joel123guz', port=5432):
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        print(f"✓ Conexión exitosa a PostgreSQL")
        print(f"  Base de datos: {database}")
        return conn
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        return None


def cargar_especies(cursor, ruta_csv):
    print(f"\n📊 Cargando especies...")
    
    try:
        contador = 0
        with open(ruta_csv, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                cursor.execute("""
                    INSERT INTO especie (nombre_cientifico, nombre_comun, reino, familia)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (nombre_cientifico) DO NOTHING
                    RETURNING id_especie
                """, (
                    row['nombre_cientifico'],
                    row['nombre_comun'],
                    row['reino'],
                    row['familia']
                ))
                
                result = cursor.fetchone()
                if result:
                    contador += 1
                    print(f"   ✓ Especie: {row['nombre_cientifico']} (ID: {result[0]})")
                else:
                    # Si ya existe, obtener su ID
                    cursor.execute(
                        "SELECT id_especie FROM especie WHERE nombre_cientifico = %s",
                        (row['nombre_cientifico'],)
                    )
                    result = cursor.fetchone()
                    if result:
                        print(f"   ⚠️  Especie ya existe: {row['nombre_cientifico']} (ID: {result[0]})")
        
        print(f"   Total nuevas: {contador}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def cargar_secuencias(cursor, ruta_csv):
    print(f"\n📊 Cargando secuencias...")
    
    try:
        contador = 0
        with open(ruta_csv, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            
            for idx, row in enumerate(reader, 1):
                # Obtener id_especie
                cursor.execute(
                    "SELECT id_especie FROM especie WHERE nombre_cientifico = %s",
                    (row['nombre_cientifico'],)
                )
                resultado = cursor.fetchone()
                
                if not resultado:
                    print(f"   ⚠️  Fila {idx}: Especie no encontrada: {row['nombre_cientifico']}")
                    continue
                
                id_especie = resultado[0]
                
                # Insertar secuencia
                cursor.execute("""
                    INSERT INTO secuencia (
                        id_especie, accession_number, descripcion,
                        tipo_secuencia, longitud, secuencia, fuente_database
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (accession_number) DO NOTHING
                    RETURNING id_secuencia
                """, (
                    id_especie,
                    row['accession_number'],
                    row['descripcion'],
                    row['tipo_secuencia'],
                    int(row['longitud']),
                    row['secuencia'],
                    row['fuente_database']
                ))
                
                result = cursor.fetchone()
                if result:
                    contador += 1
                    print(f"   ✓ Secuencia: {row['accession_number']} (ID: {result[0]}, {len(row['secuencia']):,} nt)")
                else:
                    print(f"   ⚠️  Secuencia ya existe: {row['accession_number']}")
        
        print(f"   Total nuevas: {contador}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def cargar_composicion(cursor, ruta_csv):
    print(f"\n📊 Cargando composición...")
    
    try:
        contador = 0
        with open(ruta_csv, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Obtener id_secuencia
                cursor.execute(
                    "SELECT id_secuencia FROM secuencia WHERE accession_number = %s",
                    (row['accession_number'],)
                )
                resultado = cursor.fetchone()
                
                if not resultado:
                    print(f"   ⚠️  Secuencia no encontrada: {row['accession_number']}")
                    continue
                
                id_secuencia = resultado[0]
                
                # Insertar composición
                cursor.execute("""
                    INSERT INTO composicion_nucleotidos (
                        id_secuencia, cantidad_a, cantidad_t,
                        cantidad_g, cantidad_c, porcentaje_gc
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id_secuencia) DO NOTHING
                    RETURNING id_composicion
                """, (
                    id_secuencia,
                    int(row['cantidad_a']),
                    int(row['cantidad_t']),
                    int(row['cantidad_g']),
                    int(row['cantidad_c']),
                    float(row['porcentaje_gc'])
                ))
                
                result = cursor.fetchone()
                if result:
                    contador += 1
                    print(f"   ✓ Composición: {row['accession_number']} (ID: {result[0]})")
                else:
                    print(f"   ⚠️  Composición ya existe: {row['accession_number']}")
        
        print(f"   Total nuevas: {contador}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def verificar(cursor):
    print("\n" + "="*80)
    print("VERIFICACIÓN DE DATOS CARGADOS")
    print("="*80)
    
    cursor.execute("SELECT COUNT(*) FROM especie")
    print(f"\n✓ Total especies: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM secuencia")
    print(f"✓ Total secuencias: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM composicion_nucleotidos")
    print(f"✓ Total composiciones: {cursor.fetchone()[0]}")
    
    print("\n" + "-"*80)
    print("DETALLES DE SECUENCIAS:")
    print("-"*80)
    
    cursor.execute("""
        SELECT 
            e.nombre_cientifico,
            s.accession_number,
            s.tipo_secuencia,
            s.longitud,
            c.porcentaje_gc
        FROM especie e
        JOIN secuencia s ON e.id_especie = s.id_especie
        LEFT JOIN composicion_nucleotidos c ON s.id_secuencia = c.id_secuencia
        ORDER BY s.id_secuencia
    """)
    
    for row in cursor.fetchall():
        print(f"\n  {row[1]}")
        print(f"    Especie: {row[0]}")
        print(f"    Tipo: {row[2]}")
        print(f"    Longitud: {row[3]:,} nucleótidos")
        if row[4]:
            print(f"    GC%: {row[4]:.2f}%")


def main():
    print("="*80)
    print("CARGA DE DATOS EN POSTGRESQL - VERSIÓN WINDOWS")
    print("="*80)
    
    # Configuración
    config = {
        'host': 'localhost',
        'database': 'genetica_comparada',
        'user': 'postgres',
        'password': 'joel123guz',
        'port': 5432
    }
    
    print("\n📋 Configuración:")
    print(f"   Database: {config['database']}")
    print(f"   User: {config['user']}")
    print(f"   Port: {config['port']}")
    
    # Conectar
    print("\n" + "="*80)
    print("PASO 1: CONEXIÓN")
    print("="*80)
    
    conn = conectar_postgres(**config)
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Buscar archivos CSV
        if os.path.exists('csv/especie.csv'):
            dir_csv = 'csv'
        elif os.path.exists('especie.csv'):
            dir_csv = '.'
        else:
            print("❌ No se encontraron archivos CSV")
            print("   Asegúrate de estar en el directorio correcto")
            return
        
        print(f"\n📂 Directorio CSV: {dir_csv}")
        
        csv_especie = os.path.join(dir_csv, 'especie.csv')
        csv_secuencia = os.path.join(dir_csv, 'secuencia.csv')
        csv_composicion = os.path.join(dir_csv, 'composicion_nucleotidos.csv')
        
        # Cargar datos
        print("\n" + "="*80)
        print("PASO 2: CARGA DE DATOS")
        print("="*80)
        
        exito = True
        
        # 1. Especies
        if os.path.exists(csv_especie):
            exito = cargar_especies(cursor, csv_especie) and exito
        else:
            print(f"❌ No encontrado: {csv_especie}")
            exito = False
        
        # 2. Secuencias
        if os.path.exists(csv_secuencia):
            exito = cargar_secuencias(cursor, csv_secuencia) and exito
        else:
            print(f"❌ No encontrado: {csv_secuencia}")
            exito = False
        
        # 3. Composición
        if os.path.exists(csv_composicion):
            exito = cargar_composicion(cursor, csv_composicion) and exito
        else:
            print(f"❌ No encontrado: {csv_composicion}")
            exito = False
        
        if exito:
            conn.commit()
            print("\n✓ Cambios confirmados en la base de datos")
            
            # Verificar
            verificar(cursor)
            
            print("\n" + "="*80)
            print("✅ CARGA COMPLETADA EXITOSAMENTE")
            print("="*80)
        else:
            conn.rollback()
            print("\n❌ Errores detectados - Cambios revertidos")
        
        cursor.close()
        
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()
        print("\n✓ Conexión cerrada")


if __name__ == "__main__":
    main()