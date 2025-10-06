import pandas as pd
import psycopg2
from psycopg2 import sql
db_config = {
    'dbname': 'clima_agro',
    'user': 'postgres',
    'password': 'joel123guz',
    'host': 'localhost',
    'port': '5432'
}

csv_file = 'datos_guayas.csv'

df = pd.read_csv(csv_file, delimiter=';')

df.columns = df.columns.str.strip()

try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Conexión exitosa a la base de datos PostgreSQL")

    # Crear la tabla "lecturas" si no existe
    create_table_query = "CREATE TABLE IF NOT EXISTS lecturas (id SERIAL PRIMARY KEY);"
    cursor.execute(create_table_query)
    conn.commit()

    # Crear columnas dinámicamente según las columnas del CSV
    for column in df.columns:
        # Definir un tipo de dato general (TEXT) para todas las columnas
        alter_table_query = sql.SQL("""
            ALTER TABLE lecturas
            ADD COLUMN IF NOT EXISTS {} TEXT;
        """).format(sql.Identifier(column))  # Usar sql.Identifier para evitar problemas con nombres
        cursor.execute(alter_table_query)
    conn.commit()

    print("Columnas creadas o ya existen.")

    # Insertar datos del DataFrame en la tabla "lecturas"
    for index, row in df.iterrows():
        # Preparar la consulta de inserción
        insert_query = sql.SQL("""
            INSERT INTO lecturas ({})
            VALUES ({})
        """).format(
            sql.SQL(', ').join(map(sql.Identifier, df.columns)),  # Usamos los nombres de las columnas
            sql.SQL(', ').join([sql.Placeholder()] * len(df.columns))  # Para cada valor de columna
        )
        # Ejecutar la consulta con los valores de cada fila
        cursor.execute(insert_query, tuple(row))
    conn.commit()
    print(f"Datos insertados correctamente: {len(df)} filas")

except Exception as e:
    print(f"Error: {e}")

finally:
    if conn:
        cursor.close()
        conn.close()
        print("Conexión cerrada")
