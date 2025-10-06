import pandas as pd
import psycopg2

db_config = {
    'dbname': 'clima_agro',
    'user': 'postgres',
    'password': 'joel123guz',
    'host': 'localhost',
    'port': '5432'
}

try:
    conn = psycopg2.connect(**db_config)
    print("Conexión exitosa a la base de datos PostgreSQL")

    # Leer los datos desde la tabla 'lecturas' en un DataFrame de pandas
    query = "SELECT * FROM lecturas;"  # Aquí puedes cambiar la consulta según lo que se necesite
    df = pd.read_sql(query, conn)  # Leer los datos directamente desde PostgreSQL

    # Mostrar los primeros registros
    print(df.head())

except Exception as e:
    print(f"Error: {e}")

finally:
    if conn:
        conn.close()
        print("Conexión cerrada")
