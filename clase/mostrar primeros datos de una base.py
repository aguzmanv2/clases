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

    query = "SELECT * FROM lecturas;"
    df = pd.read_sql(query, conn)

    # Mostrar los primeros 5 registros
    print("Primeros registros:")
    print(df.head())

    # Obtener estadísticas descriptivas
    print("\nEstadísticas descriptivas:")
    print(df.describe())

except Exception as e:
    print(f"Error: {e}")

finally:
    if conn:
        conn.close()
        print("Conexión cerrada")
