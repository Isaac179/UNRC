import os
import re

# Directorio de trabajo actual
DIRECTORIO = os.getcwd()

# Patrón para descartar registros contables y administrativos rutinarios
patron_ignorar = re.compile(
    r"conciliación bancaria|integración de disponibilidades|listas de raya|pago de sueldos al personal|reporte de entrega de cheques",
    re.IGNORECASE
)

# Buscar todos los archivos extraídos en la carpeta
archivos_extraidos = [f for f in os.listdir(DIRECTORIO) if f.endswith("_extraido.txt")]

if not archivos_extraidos:
    print(f"⚠️ No se encontraron archivos '*_extraido.txt' en: {DIRECTORIO}")
    exit()

for archivo in archivos_extraidos:
    ruta_entrada = os.path.join(DIRECTORIO, archivo)
    nombre_salida = archivo.replace("_extraido.txt", "_saneado.txt")
    ruta_salida = os.path.join(DIRECTORIO, nombre_salida)
    
    print(f"🧹 Saneando: {archivo}...")
    lineas_limpias = []
    
    with open(ruta_entrada, "r", encoding="utf-8") as f:
        for linea in f:
            if not patron_ignorar.search(linea):
                lineas_limpias.append(linea)
                
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.writelines(lineas_limpias)
        
    print(f"✅ Generado: {nombre_salida}")

print("\n🎉 ¡Saneamiento completado con éxito!")