# Pipeline de Procesamiento de Datos

Este directorio contiene los scripts responsables de procesar los datos de las investigaciones de la NASA.

---

## 📋 Uso

Para generar el archivo de datos final desde cero, se deben ejecutar los scripts en el siguiente orden desde la terminal.

1.  **Preparar datos iniciales y añadir IDs:**
    ```bash
    py scripts/script.py
    ```

2.  **Extraer el texto completo de las fuentes (Web Scraping):**
    ```bash
    py scripts/scrapping.py
    ```

3.  **Procesar el texto con NLP y generar Embeddings:**
    ```bash
    py scripts/nlp_script.py
    ```

---

## 💾 Archivo de Datos Final

El resultado de este pipeline es el archivo `datos_listos_para_db.json`. Debido a su gran tamaño (~340 MB), está excluido de este repositorio.

Puedes descargarlo directamente desde el siguiente enlace:

➡️ [**Descargar datos_listos_para_db.json (Google Drive)**](https://drive.google.com/file/d/1UfqN0bJLzKyMfECWhFQEu7ct3HPHqG_q/view?usp=sharing)

**Instrucción:** Una vez descargado, coloca el archivo en la carpeta `/data` del proyecto para que los siguientes procesos, como la verificación pueda funcionar correctamente.