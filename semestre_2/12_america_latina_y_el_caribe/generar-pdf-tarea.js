const fs = require('fs');
const { renderPdfFromHtml } = require('html-pdf-lite');

// Ruta a tu archivo HTML
const rutaHTML = 'C:/Users/isaac/OneDrive/Desktop/IESCDMX-Rosario-Castellanos/UNRC/semestre_2/12_america_latina_y_el_caribe/tarea4.html';

// 1. Leer el archivo HTML
const htmlCompleto = fs.readFileSync(rutaHTML, 'utf8');

// 2. Función para generar el PDF
async function generarPDF() {
  try {
    console.log('📖 Leyendo archivo HTML...');
    console.log('🔄 Generando PDF desde tarea4.html...');
    
    // Generar el PDF desde el HTML
    const pdfBuffer = await renderPdfFromHtml(htmlCompleto, {
      autoResolveFonts: true, // Usa fuentes del sistema
    });

    // Guardar el PDF en la misma carpeta que el HTML
    const rutaPDF = 'C:/Users/isaac/OneDrive/Desktop/IESCDMX-Rosario-Castellanos/UNRC/semestre_2/12_america_latina_y_el_caribe/tarea4.pdf';
    fs.writeFileSync(rutaPDF, pdfBuffer);
    
    // Mostrar información del archivo
    const stats = fs.statSync(rutaPDF);
    const tamañoKB = (stats.size / 1024).toFixed(2);
    const tamañoMB = (stats.size / (1024 * 1024)).toFixed(2);
    
    console.log('✅ ¡PDF generado exitosamente!');
    console.log(`📁 Ubicación: ${rutaPDF}`);
    console.log(`📊 Tamaño: ${tamañoKB} KB (${tamañoMB} MB)`);
    
    if (stats.size / (1024 * 1024) > 1) {
      console.log('⚠️  El PDF pesa más de 1 MB. Revisa las imágenes o contenido.');
    } else {
      console.log('🎯 ¡Perfecto! El PDF es menor a 1 MB.');
    }
    
  } catch (error) {
    console.error('❌ Error al generar el PDF:', error);
    console.error('Asegúrate de que la ruta del archivo HTML sea correcta.');
  }
}

// 3. Ejecutar la función
generarPDF();