import os
import cv2
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
import pytesseract

# ==========================================
# 1. CONFIGURACIÓN TESSERACT
# ==========================================
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

# ==========================================
# 2. RUTA DE TRABAJO (Tu carpeta de fondos primarios)
# ==========================================
DIRECTORIO_PDFS = r"C:\Users\isaac\OneDrive\Desktop\IESCDMX-Rosario-Castellanos\UNRC\semestre_3\13_derecho_internacional_publico\LIT\sre_fondo_sdocumentales_primarios"

def ocr_en_memoria(page):
    """Renderiza la página en memoria y aplica OCR con OpenCV sin guardar imagen."""
    zoom = 2
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    img_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(
        gray, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 31, 10
    )
    gray = cv2.medianBlur(gray, 3)
    
    return pytesseract.image_to_string(gray, lang="spa", config="--oem 3 --psm 3")

def procesar_pdf(ruta_pdf):
    nombre_base = os.path.splitext(os.path.basename(ruta_pdf))[0]
    ruta_txt = os.path.join(os.path.dirname(ruta_pdf), f"{nombre_base}_extraido.txt")
    
    print(f"\n==========================================")
    print(f"📄 Procesando: {os.path.basename(ruta_pdf)}")
    print(f"==========================================")
    
    try:
        doc = fitz.open(ruta_pdf)
    except Exception as e:
        print(f"❌ Error al abrir {ruta_pdf}: {e}")
        return
        
    texto_completo = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        texto_pagina = page.get_text().strip()
        
        # Si la página tiene menos de 50 caracteres, aplica OCR en memoria
        if len(texto_pagina) < 50:
            print(f"🔍 Pág. {page_num + 1}/{len(doc)}: Escaneada -> Aplicando OCR...")
            texto_pagina = ocr_en_memoria(page).strip()
        else:
            print(f"⚡ Pág. {page_num + 1}/{len(doc)}: Texto digital extraído.")
            
        if texto_pagina:
            texto_completo.append(f"\n--- PÁGINA {page_num + 1} ---\n{texto_pagina}\n")
            
    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.writelines(texto_completo)
        
    print(f"✅ Generado: {os.path.basename(ruta_txt)}")

# ==========================================
# 3. EJECUCIÓN POR LOTES
# ==========================================
if __name__ == "__main__":
    if not os.path.exists(DIRECTORIO_PDFS):
        print(f"❌ La ruta especificada no existe: {DIRECTORIO_PDFS}")
        exit()
        
    archivos = [f for f in os.listdir(DIRECTORIO_PDFS) if f.lower().endswith(".pdf")]
    
    if not archivos:
        print(f"⚠️ No se encontraron archivos .pdf en la carpeta.")
        exit()
        
    print(f"🚀 Se encontraron {len(archivos)} archivo(s) PDF para procesar.")
    for archivo in archivos:
        ruta_completa = os.path.join(DIRECTORIO_PDFS, archivo)
        procesar_pdf(ruta_completa)
        
    print(f"\n🎉 ¡Todos los documentos fueron procesados exitosamente!")