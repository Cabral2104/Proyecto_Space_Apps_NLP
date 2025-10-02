
import json
import os
import time
import spacy
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

print("Iniciando nlp_script.py v2: Procesamiento NLP y Embeddings (Chunking Mejorado)")

# --- PASO 1: CONFIGURACIÓN Y CARGA DE MODELOS ---

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_json_path = os.path.join(BASE_DIR, 'data', 'datos_texto_completo.json')
output_json_path = os.path.join(BASE_DIR, 'data', 'datos_listos_para_db.json')

try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("La variable de entorno GOOGLE_API_KEY no está configurada en el archivo .env")
    genai.configure(api_key=api_key)
    print("API Key de Google cargada correctamente.")
except Exception as e:
    print(f"Error crítico al configurar la API de Google: {e}")
    exit()

try:
    print("Cargando modelo de spaCy...")
    nlp_spacy = spacy.load("es_core_news_sm")
    print("Configurando modelo de embeddings de Gemini (text-embedding-004)...")
    model_gemini = 'models/text-embedding-004'
    print("Modelos listos.")
except Exception as e:
    print(f"Error al cargar los modelos: {e}")
    exit()

# --- PASO 2: DEFINICIÓN DE FUNCIONES (CON LA CORRECCIÓN) ---

# ------------------- INICIO DE LA CORRECCIÓN -------------------
def dividir_en_chunks(doc_spacy, max_chars: int = 8000) -> list[str]:
    """
    Divide un documento de spaCy en chunks de texto más pequeños,
    agrupando oraciones sin exceder un tamaño máximo de caracteres.
    """
    chunks = []
    chunk_actual = ""
    for sent in doc_spacy.sents:
        # Si añadir la siguiente oración excede el límite, guarda el chunk actual
        if len(chunk_actual) + len(sent.text_with_ws) > max_chars:
            if chunk_actual: # Asegurarse de no añadir chunks vacíos
                chunks.append(chunk_actual)
            chunk_actual = ""
        
        # Si la oración por sí sola es más grande que el límite, se omite (caso raro)
        if len(sent.text_with_ws) > max_chars:
            continue

        chunk_actual += sent.text_with_ws

    # Añadir el último chunk si no está vacío
    if chunk_actual:
        chunks.append(chunk_actual)
        
    return chunks
# -------------------- FIN DE LA CORRECCIÓN ---------------------

def generar_embedding_gemini(texto_chunk: str, model) -> list[float] | None:
    """Genera un embedding para un chunk de texto usando la API de Gemini."""
    try:
        if not texto_chunk.strip(): # No enviar chunks vacíos a la API
            return None
        embedding = genai.embed_content(model=model, content=texto_chunk)
        return embedding['embedding']
    except Exception as e:
        print(f"  -> ADVERTENCIA al generar embedding: {e}")
        return None

def extraer_datos_grafo_spacy(doc_spacy, study_id: int, study_title: str) -> dict:
    """Extrae nodos y relaciones de un texto procesado por spaCy."""
    nodes = []
    relationships = []
    study_node_id = f"study_{study_id}"
    nodes.append({"id": study_node_id, "label": "Study", "properties": {"title": study_title, "id": study_id}})

    for ent in doc_spacy.ents:
        ent_node_id = f"ent_{study_id}_{ent.start_char}"
        nodes.append({"id": ent_node_id, "label": ent.label_, "properties": {"name": ent.text.strip()}})
        relationships.append({"source": study_node_id, "target": ent_node_id, "type": "MENTIONS"})
        
    return {"nodes": nodes, "relationships": relationships}

# --- PASO 3: PROCESAMIENTO PRINCIPAL ---

def procesar_articulos():
    """Función principal que orquesta todo el proceso."""
    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            articulos = json.load(f)
        print(f"Se encontraron {len(articulos)} artículos para procesar.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de entrada: {input_json_path}")
        return

    resultados_finales = {"articles": []}

    for articulo in articulos:
        article_id = articulo.get('id', 'N/A')
        title = articulo.get('Title', 'Sin Título')
        full_text = articulo.get('full_text', '')

        print(f"\n--- Procesando Artículo ID: {article_id} | Título: {title[:50]}... ---")

        articulo_procesado = {
            "id": article_id, "title": title, "link": articulo.get('Link'),
            "graph_data": {}, "semantic_data": []
        }

        if full_text and full_text.strip():
            doc = nlp_spacy(full_text)
            
            # 1. Procesamiento con spaCy (para el grafo)
            articulo_procesado["graph_data"] = extraer_datos_grafo_spacy(doc, article_id, title)
            print(f"-> Grafo: Se extrajeron {len(articulo_procesado['graph_data']['nodes'])} nodos.")

            # 2. Chunking y Embeddings (usando la nueva función)
            chunks = dividir_en_chunks(doc) # Le pasamos el documento de spaCy
            print(f"-> Semántica: El texto se dividió en {len(chunks)} chunks.")
            for i, chunk in enumerate(chunks):
                print(f"  - Generando embedding para chunk {i+1}/{len(chunks)}...")
                embedding_vector = generar_embedding_gemini(chunk, model_gemini)
                if embedding_vector:
                    articulo_procesado["semantic_data"].append({
                        "chunk_text": chunk, "embedding_vector": embedding_vector
                    })
                time.sleep(1)
        else:
            print("-> AVISO: No se encontró texto completo válido. Se omitirá el procesamiento NLP.")

        resultados_finales["articles"].append(articulo_procesado)

    try:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(resultados_finales, f, indent=4, ensure_ascii=False)
        print(f"\n¡PROCESO COMPLETADO! Los datos listos para la DB se han guardado en: {output_json_path}")
    except Exception as e:
        print(f"Error al guardar el archivo JSON final: {e}")

if __name__ == "__main__":
    procesar_articulos()