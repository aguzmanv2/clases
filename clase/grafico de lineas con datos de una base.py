import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# Datos de conexión a PostgreSQL
db_config = {
    'dbname': 'clima_agro',
    'user': 'postgres',
    'password': 'joel123guz',
    'host': 'localhost',  # O la dirección IP del servidor
    'port': '5432'  # Puerto por defecto de PostgreSQL
}

# Conectar a la base de datos PostgreSQL
try:
    conn = psycopg2.connect(**db_config)
    print("Conexión exitosa a la base de datos PostgreSQL")

    # Leer los datos desde la tabla 'lecturas' en un DataFrame de pandas
    query = "SELECT * FROM lecturas;"  # Aquí puedes cambiar la consulta según lo necesites
    df = pd.read_sql(query, conn)  # Leer los datos directamente desde PostgreSQL

    # Verificar los nombres de las columnas
    print("Nombres de las columnas:")
    print(df.columns)

    # Mostrar los primeros registros
    print("\nPrimeros registros:")
    print(df.head())

    # Graficar los datos
    plt.figure(figsize=(10,6))

    # Usar los nombres correctos de las columnas para graficar
    plt.plot(df['DOY'], df['T2M'], label='Temperatura (T2M)', color='blue')
    plt.plot(df['DOY'], df['RH2M'], label='Humedad Relativa (RH2M)', color='green')

    # Añadir título y etiquetas
    plt.title('Temperatura y Humedad Relativa a lo largo del Año')
    plt.xlabel('Día del Año (DOY)')
    plt.ylabel('Valor')

    # Añadir leyenda
    plt.legend()

    # Mostrar el gráfico
    plt.grid(True)
    plt.show()

except Exception as e:
    print(f"Error: {e}")

finally:
    # Cerrar la conexión
    if conn:
        conn.close()
        print("Conexión cerrada")
