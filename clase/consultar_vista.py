import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os


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


def consultar_vista_comparacion_gc(conn):
    query = """
    SELECT 
        nombre_cientifico,
        nombre_comun,
        accession_number,
        tipo_secuencia,
        longitud,
        porcentaje_gc,
        clasificacion_gc,
        cantidad_a,
        cantidad_t,
        cantidad_g,
        cantidad_c
    FROM comparacion_gc
    ORDER BY nombre_cientifico, accession_number;
    """
    
    try:
        df = pd.read_sql_query(query, conn)
        print(f"\n✓ Datos consultados: {len(df)} registros")
        return df
    except Exception as e:
        print(f"❌ Error al consultar vista: {e}")
        return None


def generar_grafico_barras_gc(df, output_dir='resultados'):
    print("\n📊 Generando gráfico de barras...")
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Configurar estilo
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 6)
    
    # Crear figura
    fig, ax = plt.subplots()
    
    # Crear etiquetas para el eje X
    df['etiqueta'] = df['accession_number'] + '\n' + df['nombre_cientifico']
    
    # Crear barras
    colores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
    bars = ax.bar(df['etiqueta'], df['porcentaje_gc'], 
                   color=colores[:len(df)], 
                   edgecolor='black', 
                   linewidth=1.5)
    
    # Agregar valores encima de las barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Personalizar el gráfico
    ax.set_xlabel('Secuencia / Especie', fontsize=12, fontweight='bold')
    ax.set_ylabel('Contenido GC (%)', fontsize=12, fontweight='bold')
    ax.set_title('Comparación de Contenido GC entre Secuencias', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Línea de referencia (promedio)
    promedio_gc = df['porcentaje_gc'].mean()
    ax.axhline(y=promedio_gc, color='red', linestyle='--', 
               linewidth=2, label=f'Promedio: {promedio_gc:.2f}%')
    
    # Rango óptimo de GC para plantas (ejemplo: 35-45%)
    ax.axhspan(35, 45, alpha=0.1, color='green', 
               label='Rango típico plantas')
    
    # Leyenda
    ax.legend(loc='upper right', fontsize=10)
    
    # Ajustar diseño
    plt.xticks(rotation=0, ha='center')
    plt.tight_layout()
    
    # Guardar
    archivo = os.path.join(output_dir, 'grafico_contenido_gc.png')
    plt.savefig(archivo, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico guardado: {archivo}")
    
    plt.close()


def generar_grafico_composicion_nucleotidos(df, output_dir='resultados'):
    print("\n📊 Generando gráfico de composición de nucleótidos...")
    
    # Crear figura con subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfico 1: Barras agrupadas
    ax1 = axes[0]
    x = range(len(df))
    width = 0.2
    
    ax1.bar([i - 1.5*width for i in x], df['cantidad_a'], width, 
            label='Adenina (A)', color='#3498db')
    ax1.bar([i - 0.5*width for i in x], df['cantidad_t'], width, 
            label='Timina (T)', color='#e74c3c')
    ax1.bar([i + 0.5*width for i in x], df['cantidad_g'], width, 
            label='Guanina (G)', color='#2ecc71')
    ax1.bar([i + 1.5*width for i in x], df['cantidad_c'], width, 
            label='Citosina (C)', color='#f39c12')
    
    ax1.set_xlabel('Secuencia', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Cantidad de Bases', fontsize=12, fontweight='bold')
    ax1.set_title('Composición de Nucleótidos por Secuencia', 
                  fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(df['accession_number'])
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Gráfico 2: Gráfico de pie (primera secuencia como ejemplo)
    ax2 = axes[1]
    if len(df) > 0:
        idx = 0
        bases = [df.iloc[idx]['cantidad_a'], 
                 df.iloc[idx]['cantidad_t'],
                 df.iloc[idx]['cantidad_g'], 
                 df.iloc[idx]['cantidad_c']]
        labels = ['Adenina (A)', 'Timina (T)', 'Guanina (G)', 'Citosina (C)']
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        
        wedges, texts, autotexts = ax2.pie(bases, labels=labels, colors=colors,
                                             autopct='%1.1f%%', startangle=90)
        
        # Mejorar texto
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        ax2.set_title(f'Distribución de Bases\n{df.iloc[idx]["accession_number"]}', 
                      fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    
    # Guardar
    archivo = os.path.join(output_dir, 'grafico_composicion_nucleotidos.png')
    plt.savefig(archivo, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico guardado: {archivo}")
    
    plt.close()


def generar_grafico_comparativo_gc_longitud(df, output_dir='resultados'):
    print("\n📊 Generando gráfico comparativo GC% vs Longitud...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Scatter plot
    scatter = ax.scatter(df['longitud'], df['porcentaje_gc'], 
                         s=200, c=df['porcentaje_gc'], 
                         cmap='viridis', 
                         edgecolors='black', linewidth=1.5, 
                         alpha=0.7)
    
    # Etiquetas para cada punto
    for idx, row in df.iterrows():
        ax.annotate(row['accession_number'], 
                    (row['longitud'], row['porcentaje_gc']),
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=9, 
                    bbox=dict(boxstyle='round,pad=0.3', 
                             facecolor='yellow', alpha=0.5))
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Contenido GC (%)', fontsize=11, fontweight='bold')
    
    # Etiquetas
    ax.set_xlabel('Longitud de la Secuencia (nucleótidos)', 
                  fontsize=12, fontweight='bold')
    ax.set_ylabel('Contenido GC (%)', fontsize=12, fontweight='bold')
    ax.set_title('Relación entre Longitud de Secuencia y Contenido GC', 
                 fontsize=14, fontweight='bold', pad=20)
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Guardar
    archivo = os.path.join(output_dir, 'grafico_gc_vs_longitud.png')
    plt.savefig(archivo, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico guardado: {archivo}")
    
    plt.close()


def exportar_a_csv(df, output_dir='resultados'):
    print("\n💾 Exportando datos a CSV...")
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Generar nombre con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archivo = os.path.join(output_dir, f'comparacion_gc_{timestamp}.csv')
    
    # Exportar
    df.to_csv(archivo, index=False, encoding='utf-8')
    print(f"✓ Datos exportados: {archivo}")
    print(f"  Registros: {len(df)}")
    print(f"  Columnas: {len(df.columns)}")
    
    return archivo


def generar_estadisticas_resumen(df, output_dir='resultados'):
    print("\n📋 Generando resumen estadístico...")
    
    archivo = os.path.join(output_dir, 'estadisticas_resumen.txt')
    
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RESUMEN ESTADÍSTICO - ANÁLISIS DE CONTENIDO GC\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total de secuencias analizadas: {len(df)}\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("ESTADÍSTICAS DE CONTENIDO GC\n")
        f.write("-" * 80 + "\n")
        f.write(f"GC% Promedio: {df['porcentaje_gc'].mean():.2f}%\n")
        f.write(f"GC% Mínimo: {df['porcentaje_gc'].min():.2f}%\n")
        f.write(f"GC% Máximo: {df['porcentaje_gc'].max():.2f}%\n")
        f.write(f"Desviación estándar: {df['porcentaje_gc'].std():.2f}%\n")
        f.write(f"Rango: {df['porcentaje_gc'].max() - df['porcentaje_gc'].min():.2f}%\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("ESTADÍSTICAS DE LONGITUD\n")
        f.write("-" * 80 + "\n")
        f.write(f"Longitud Promedio: {df['longitud'].mean():,.0f} nucleótidos\n")
        f.write(f"Longitud Mínima: {df['longitud'].min():,} nucleótidos\n")
        f.write(f"Longitud Máxima: {df['longitud'].max():,} nucleótidos\n")
        f.write(f"Longitud Total: {df['longitud'].sum():,} nucleótidos\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("DETALLE POR SECUENCIA\n")
        f.write("-" * 80 + "\n\n")
        
        for idx, row in df.iterrows():
            f.write(f"Secuencia: {row['accession_number']}\n")
            f.write(f"  Especie: {row['nombre_cientifico']} ({row['nombre_comun']})\n")
            f.write(f"  Tipo: {row['tipo_secuencia']}\n")
            f.write(f"  Longitud: {row['longitud']:,} nucleótidos\n")
            f.write(f"  Contenido GC: {row['porcentaje_gc']:.2f}%\n")
            f.write(f"  Clasificación: {row['clasificacion_gc']}\n")
            f.write(f"  Composición:\n")
            f.write(f"    - Adenina (A): {row['cantidad_a']:,} ({row['cantidad_a']/row['longitud']*100:.2f}%)\n")
            f.write(f"    - Timina (T): {row['cantidad_t']:,} ({row['cantidad_t']/row['longitud']*100:.2f}%)\n")
            f.write(f"    - Guanina (G): {row['cantidad_g']:,} ({row['cantidad_g']/row['longitud']*100:.2f}%)\n")
            f.write(f"    - Citosina (C): {row['cantidad_c']:,} ({row['cantidad_c']/row['longitud']*100:.2f}%)\n")
            f.write("\n")
        
        f.write("="*80 + "\n")
        f.write("FIN DEL RESUMEN\n")
        f.write("="*80 + "\n")
    
    print(f"✓ Resumen guardado: {archivo}")


def main():
    print("="*80)
    print("SESIÓN 4 - ACTIVIDAD 2: ANÁLISIS Y VISUALIZACIÓN DE CONTENIDO GC")
    print("="*80)
    
    # Configuración
    config = {
        'host': 'localhost',
        'database': 'genetica_comparada',
        'user': 'postgres',
        'password': 'joel123guz',
        'port': 5432
    }
    
    output_dir = 'resultados'
    
    print(f"\n📋 Configuración:")
    print(f"   Database: {config['database']}")
    print(f"   Directorio de salida: {output_dir}/")
    
    # Conectar
    print("\n" + "="*80)
    print("PASO 1: CONEXIÓN A POSTGRESQL")
    print("="*80)
    
    conn = conectar_postgres(**config)
    if not conn:
        return
    
    try:
        # Consultar vista
        print("\n" + "="*80)
        print("PASO 2: CONSULTAR VISTA comparacion_gc")
        print("="*80)
        
        df = consultar_vista_comparacion_gc(conn)
        if df is None or len(df) == 0:
            print("❌ No se encontraron datos")
            return
        
        # Mostrar preview
        print("\n📊 Vista previa de los datos:")
        print(df[['accession_number', 'nombre_cientifico', 
                  'longitud', 'porcentaje_gc']].to_string())
        
        # Generar gráficos
        print("\n" + "="*80)
        print("PASO 3: GENERAR GRÁFICOS")
        print("="*80)
        
        generar_grafico_barras_gc(df, output_dir)
        generar_grafico_composicion_nucleotidos(df, output_dir)
        generar_grafico_comparativo_gc_longitud(df, output_dir)
        
        # Exportar a CSV
        print("\n" + "="*80)
        print("PASO 4: EXPORTAR DATOS")
        print("="*80)
        
        archivo_csv = exportar_a_csv(df, output_dir)
        generar_estadisticas_resumen(df, output_dir)
        
        # Resumen final
        print("\n" + "="*80)
        print("✅ PROCESO COMPLETADO")
        print("="*80)
        print(f"\nArchivos generados en '{output_dir}/':")
        print("  📊 grafico_contenido_gc.png")
        print("  📊 grafico_composicion_nucleotidos.png")
        print("  📊 grafico_gc_vs_longitud.png")
        print(f"  💾 {os.path.basename(archivo_csv)}")
        print("  📋 estadisticas_resumen.txt")
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()
        print("✓ Conexión cerrada")


if __name__ == "__main__":
    main()