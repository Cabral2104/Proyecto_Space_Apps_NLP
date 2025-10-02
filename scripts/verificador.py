
import json
import os

print("--- Verificador de Artículos en JSON Final ---")

# --- Configuración de Rutas ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_json_path = os.path.join(BASE_DIR, 'data', 'datos_listos_para_db.json')

# --- Carga de Datos ---
try:
    print(f"Cargando el archivo: {input_json_path}")
    with open(input_json_path, 'r', encoding='utf-8') as f:
        
        data = json.load(f) 
    
    articles_list = data.get("articles", [])
    print(f"¡Carga completa! Se encontraron {len(articles_list)} artículos en el archivo.")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta: {input_json_path}")
    exit()
except json.JSONDecodeError:
    print("Error: El archivo no es un JSON válido. Puede que el proceso anterior no haya terminado correctamente.")
    exit()

# --- Bucle de Búsqueda Interactivo ---
while True:
    id_a_buscar = input("\nIntroduce el ID del artículo que quieres verificar (o escribe 'salir' para terminar): ")

    if id_a_buscar.lower() == 'salir':
        print("Saliendo del verificador. ¡Hasta luego!")
        break

    try:
        id_num = int(id_a_buscar)
    except ValueError:
        print("Error: Por favor, introduce un número válido.")
        continue

    articulo_encontrado = None
    for articulo in articles_list:
        if articulo.get("id") == id_num:
            articulo_encontrado = articulo
            break

    if articulo_encontrado:
        titulo = articulo_encontrado.get('title', 'Sin Título')
        print(f"✅ ¡ÉXITO! Se encontró el artículo con ID {id_num}.")
        print(f"   Título: {titulo}")
    else:
        print(f"❌ FALLO. No se encontró ningún artículo con el ID {id_num} en el archivo.")