
import pandas as pd
import os

print("Iniciando script.py: Lector de CSV con asignación de ID")

# --- Configuración de Rutas ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_csv_path = os.path.join(BASE_DIR, 'data', 'SB_publication_PMC.csv')
output_json_path = os.path.join(BASE_DIR, 'data', 'salida.json')

# --- Lectura y Conversión ---
try:
    # Lee el archivo CSV usando Pandas
    print(f"Leyendo el archivo CSV desde: {input_csv_path}")
    df = pd.read_csv(input_csv_path)


    # .insert(0, ...) la coloca como la primera columna, lo cual es más ordenado.
    df.insert(0, 'id', df.index + 1)
    print("Se ha añadido una columna 'id' única a cada artículo.")


    # Convierte el DataFrame a formato JSON (orient='records' crea una lista de objetos)
    print(f"Convirtiendo datos a JSON...")
    # Asegurar de que las columnas tengan nombres consistentes, en este caso 'title' y 'link'
    df.to_json(output_json_path, orient='records', indent=4, force_ascii=False)

    print(f"¡Éxito! Los datos han sido guardados con su ID en: {output_json_path}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta: {input_csv_path}")
    print("Asegúrate de que 'tu_archivo.csv' exista en la carpeta /data/")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")