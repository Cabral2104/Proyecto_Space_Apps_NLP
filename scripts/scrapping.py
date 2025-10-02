# scripts/scrapping.py

import json
import requests
from bs4 import BeautifulSoup
import os

print("Iniciando scrapping.py: Extractor de Texto Completo desde Links")

# --- Configuración de Rutas ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_json_path = os.path.join(BASE_DIR, 'data', 'salida.json')
output_json_path = os.path.join(BASE_DIR, 'data', 'datos_texto_completo.json')

# --- Encabezados para simular un navegador ---
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# --- Proceso de Web Scraping ---
try:
    print(f"Leyendo el archivo JSON desde: {input_json_path}")
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    datos_completos = []

    print(f"Iniciando web scraping para {len(data)} registros...")
    for i, registro in enumerate(data):
        
        
        nombre_columna_link = 'Link' 
        link = registro.get(nombre_columna_link) 

        print(f"\n({i+1}/{len(data)}) Procesando registro ID: {registro.get('id')}")

        if link and isinstance(link, str) and link.startswith('http'):
            print(f"-> Link encontrado: {link}")
            try:
                response = requests.get(link, headers=headers, timeout=15)
                print(f"-> Estado de la respuesta del servidor: {response.status_code}")
                
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')
                
                text_elements = soup.find_all('p') 
                article_text = ' '.join([p.get_text(strip=True) for p in text_elements])

                if not article_text:
                    body = soup.find('body')
                    if body:
                        article_text = body.get_text(strip=True)

                registro['full_text'] = article_text
                print(f"-> Éxito: Texto extraído.")

            except requests.RequestException as e:
                registro['full_text'] = f"Error al scrapear: {e}"
                print(f"-> ERROR al acceder al link: {e}")
        else:
            registro['full_text'] = "No se proporcionó un link válido en el JSON."
            print(f"-> AVISO: Omitiendo registro. El link no es válido o la columna '{nombre_columna_link}' es incorrecta.")
        
        datos_completos.append(registro)

    print("\n----------------------------------------------------")
    print(f"Guardando los datos completos en: {output_json_path}")
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(datos_completos, f, indent=4, ensure_ascii=False)

    print("¡Proceso de scraping completado!")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta: {input_json_path}")
    print("Asegúrate de haber ejecutado 'script.py' primero.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")