import csv
import os
from datetime import datetime


def analizar_fasta(ruta_archivo):
    
    print(f"\n📄 Analizando: {os.path.basename(ruta_archivo)}")
    
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    
    # Extraer el encabezado (primera línea que empieza con >)
    encabezado = lineas[0].strip()
    
    # Extraer el ID (accession number)
    accession_number = encabezado.split()[0][1:]  # Quitar el símbolo >
    
    # Extraer la descripción completa
    partes_encabezado = encabezado.split(None, 1)
    descripcion = partes_encabezado[1] if len(partes_encabezado) > 1 else ""
    
    # Extraer el nombre científico de la descripción
    # Formato típico: "Especie genero tipo, descripción"
    nombre_cientifico = None
    if "Zea mays" in descripcion:
        nombre_cientifico = "Zea mays"
    
    # Determinar tipo de secuencia
    tipo_secuencia = "chloroplast genome" if "chloroplast" in descripcion.lower() else "genome"
    
    # Extraer la secuencia (todas las líneas después del encabezado)
    secuencia = ""
    for linea in lineas[1:]:
        linea = linea.strip()
        if linea and not linea.startswith('>'):
            secuencia += linea
    
    # Calcular longitud y composición
    longitud = len(secuencia)
    cantidad_a = secuencia.count('A')
    cantidad_t = secuencia.count('T')
    cantidad_g = secuencia.count('G')
    cantidad_c = secuencia.count('C')
    
    # Calcular porcentaje GC
    if longitud > 0:
        porcentaje_gc = ((cantidad_g + cantidad_c) / longitud) * 100
    else:
        porcentaje_gc = 0
    
    print(f"   ✓ Accession: {accession_number}")
    print(f"   ✓ Longitud: {longitud:,} nucleótidos")
    print(f"   ✓ GC content: {porcentaje_gc:.2f}%")
    
    return {
        'accession_number': accession_number,
        'nombre_cientifico': nombre_cientifico,
        'descripcion': descripcion,
        'tipo_secuencia': tipo_secuencia,
        'longitud': longitud,
        'secuencia': secuencia,
        'cantidad_a': cantidad_a,
        'cantidad_t': cantidad_t,
        'cantidad_g': cantidad_g,
        'cantidad_c': cantidad_c,
        'porcentaje_gc': round(porcentaje_gc, 2)
    }


def crear_csv_especie(datos_secuencias, ruta_salida):
    
    print("\n📊 Creando CSV de especies...")
    
    # Extraer especies únicas
    especies_dict = {}
    for dato in datos_secuencias:
        nombre = dato['nombre_cientifico']
        if nombre and nombre not in especies_dict:
            especies_dict[nombre] = {
                'nombre_cientifico': nombre,
                'nombre_comun': 'Maíz' if nombre == 'Zea mays' else '',
                'reino': 'Plantae' if nombre == 'Zea mays' else '',
                'familia': 'Poaceae' if nombre == 'Zea mays' else ''
            }
    
    # Escribir CSV
    with open(ruta_salida, 'w', newline='', encoding='utf-8') as archivo:
        columnas = ['nombre_cientifico', 'nombre_comun', 'reino', 'familia']
        writer = csv.DictWriter(archivo, fieldnames=columnas)
        writer.writeheader()
        
        for especie in especies_dict.values():
            writer.writerow(especie)
    
    print(f"   ✓ Archivo creado: {ruta_salida}")
    print(f"   ✓ Especies registradas: {len(especies_dict)}")


def crear_csv_secuencia(datos_secuencias, ruta_salida):
    print("\n📊 Creando CSV de secuencias...")
    
    with open(ruta_salida, 'w', newline='', encoding='utf-8') as archivo:
        columnas = [
            'nombre_cientifico', 'accession_number', 'descripcion',
            'tipo_secuencia', 'longitud', 'secuencia', 'fuente_database'
        ]
        writer = csv.DictWriter(archivo, fieldnames=columnas)
        writer.writeheader()
        
        for dato in datos_secuencias:
            writer.writerow({
                'nombre_cientifico': dato['nombre_cientifico'],
                'accession_number': dato['accession_number'],
                'descripcion': dato['descripcion'],
                'tipo_secuencia': dato['tipo_secuencia'],
                'longitud': dato['longitud'],
                'secuencia': dato['secuencia'],
                'fuente_database': 'NCBI'
            })
    
    print(f"   ✓ Archivo creado: {ruta_salida}")
    print(f"   ✓ Secuencias registradas: {len(datos_secuencias)}")


def crear_csv_composicion(datos_secuencias, ruta_salida):
    print("\n📊 Creando CSV de composición de nucleótidos...")
    
    with open(ruta_salida, 'w', newline='', encoding='utf-8') as archivo:
        columnas = [
            'accession_number', 'cantidad_a', 'cantidad_t',
            'cantidad_g', 'cantidad_c', 'porcentaje_gc'
        ]
        writer = csv.DictWriter(archivo, fieldnames=columnas)
        writer.writeheader()
        
        for dato in datos_secuencias:
            writer.writerow({
                'accession_number': dato['accession_number'],
                'cantidad_a': dato['cantidad_a'],
                'cantidad_t': dato['cantidad_t'],
                'cantidad_g': dato['cantidad_g'],
                'cantidad_c': dato['cantidad_c'],
                'porcentaje_gc': dato['porcentaje_gc']
            })
    
    print(f"   ✓ Archivo creado: {ruta_salida}")
    print(f"   ✓ Composiciones registradas: {len(datos_secuencias)}")


def main():
    print("="*80)
    print("CONVERSIÓN DE FASTA A CSV Y CARGA EN POSTGRESQL")
    print("="*80)
    
    # Rutas de archivos FASTA
    archivos_fasta = [
        'especie1.fasta',
        'especie2.fasta'
    ]
    
    # Directorio de salida para CSV
    dir_salida = 'csv'
    
    # Analizar todos los archivos FASTA
    print("\n" + "="*80)
    print("PASO 1: ANÁLISIS DE ARCHIVOS FASTA")
    print("="*80)
    
    datos_secuencias = []
    for archivo in archivos_fasta:
        if os.path.exists(archivo):
            datos = analizar_fasta(archivo)
            datos_secuencias.append(datos)
        else:
            print(f"⚠️  Archivo no encontrado: {archivo}")
    
    if not datos_secuencias:
        print("\n❌ No se encontraron archivos FASTA para procesar")
        return
    
    # Crear archivos CSV
    print("\n" + "="*80)
    print("PASO 2: GENERACIÓN DE ARCHIVOS CSV")
    print("="*80)
    
    csv_especie = os.path.join(dir_salida, 'especie.csv')
    csv_secuencia = os.path.join(dir_salida, 'secuencia.csv')
    csv_composicion = os.path.join(dir_salida, 'composicion_nucleotidos.csv')
    
    crear_csv_especie(datos_secuencias, csv_especie)
    crear_csv_secuencia(datos_secuencias, csv_secuencia)
    crear_csv_composicion(datos_secuencias, csv_composicion)
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE ARCHIVOS GENERADOS")
    print("="*80)
    print(f"✓ {csv_especie}")
    print(f"✓ {csv_secuencia}")
    print(f"✓ {csv_composicion}")
    
    print("\n" + "="*80)
    print("SIGUIENTE PASO: CARGAR EN POSTGRESQL")
    print("="*80)
    print("\nPara cargar los datos en PostgreSQL, usa el script:")
    print("  python3 cargar_postgresql.py")
    print("\nO ejecuta manualmente los comandos SQL de carga.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()