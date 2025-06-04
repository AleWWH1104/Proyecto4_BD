# app/test_connection.py
from database import test_connection, execute_query_to_dataframe  # Elimina el punto .

if __name__ == "__main__":
    # Probar conexión básica
    print("Probando conexión a la base de datos...")
    connection_ok = test_connection()
    
    if connection_ok:
        print("\nProbando conexion a db:")
        df = execute_query_to_dataframe("SELECT current_database();")
        print("\nResultado de la consulta:")
        print(df.head())