import os
from pathlib import Path


def analizar_fasta(ruta_archivo):
    print(f"\n{'='*80}")
    print(f"Analizando: {os.path.basename(ruta_archivo)}")
    print(f"{'='*80}\n")
    
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    encabezado = lineas[0].strip()
    
    id_secuencia = encabezado.split()[0][1:] 
    
    partes_encabezado = encabezado.split(None, 1)  
    descripcion = partes_encabezado[1] if len(partes_encabezado) > 1 else ""
    
    secuencia = ""
    for linea in lineas[1:]:
        linea = linea.strip()
        if linea and not linea.startswith('>'):
            secuencia += linea
    
    longitud = len(secuencia)
    
    print("📌 ID (Accession Number):")
    print(f"   {id_secuencia}\n")
    
    print("📌 Encabezado completo:")
    print(f"   {encabezado}\n")
    
    print("📌 Descripción:")
    print(f"   {descripcion}\n")
    
    print("📌 Longitud de la secuencia:")
    print(f"   {longitud:,} nucleótidos\n")
    
    print("📌 Primeros 100 caracteres de la secuencia:")
    print(f"   {secuencia[:100]}...\n")
    
    print("📌 Últimos 100 caracteres de la secuencia:")
    print(f"   ...{secuencia[-100:]}\n")
    
    composicion = {
        'A': secuencia.count('A'),
        'T': secuencia.count('T'),
        'G': secuencia.count('G'),
        'C': secuencia.count('C')
    }
    
    print("📊 Composición de nucleótidos:")
    for nucleotido, cantidad in composicion.items():
        porcentaje = (cantidad / longitud) * 100 if longitud > 0 else 0
        print(f"   {nucleotido}: {cantidad:,} ({porcentaje:.2f}%)")
    
    print(f"\n{'='*80}\n")
    
    return {
        'archivo': os.path.basename(ruta_archivo),
        'id': id_secuencia,
        'encabezado': encabezado,
        'descripcion': descripcion,
        'secuencia': secuencia,
        'longitud': longitud,
        'composicion': composicion
    }


def main():
    print("\n" + "="*80)
    print("ANÁLISIS DE ARCHIVOS FASTA - ACTIVIDAD 2")
    print("="*80)
    
    archivos = [
        'especie1.fasta',
        'especie2.fasta'
    ]
    
    resultados = []
    
    for archivo in archivos:
        if os.path.exists(archivo):
            resultado = analizar_fasta(archivo)
            resultados.append(resultado)
        else:
            print(f"⚠️ Archivo no encontrado: {archivo}\n")
    
    if len(resultados) == 2:
        print("\n" + "="*80)
        print("COMPARACIÓN ENTRE ESPECIES")
        print("="*80 + "\n")
        
        print(f"Especie 1: {resultados[0]['id']}")
        print(f"Especie 2: {resultados[1]['id']}\n")
        
        print(f"Longitud Especie 1: {resultados[0]['longitud']:,} nucleótidos")
        print(f"Longitud Especie 2: {resultados[1]['longitud']:,} nucleótidos")
        diferencia = abs(resultados[0]['longitud'] - resultados[1]['longitud'])
        print(f"Diferencia: {diferencia:,} nucleótidos\n")
        
        seq1 = resultados[0]['secuencia']
        seq2 = resultados[1]['secuencia']
        longitud_min = min(len(seq1), len(seq2))
        
        coincidencias = sum(1 for i in range(longitud_min) if seq1[i] == seq2[i])
        similitud = (coincidencias / longitud_min) * 100 if longitud_min > 0 else 0
        
        print(f"Similitud de secuencias: {similitud:.2f}%")
        print(f"(Basado en los primeros {longitud_min:,} nucleótidos)\n")
        
        print("="*80 + "\n")


if __name__ == "__main__":
    main()