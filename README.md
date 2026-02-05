# Video Frame Extractor CLI - Versión OpenCV 🎬

Script CLI profesional en Python para extraer frames de videos MP4 como imágenes JPG usando OpenCV.

## 🌟 Características

- ✨ **Extracción inteligente**: Frames espaciados uniformemente (no consecutivos)
- 🎨 **Redimensionamiento avanzado**: Mantiene proporción con padding automático
- 📊 **Barra de progreso**: Visualización en tiempo real del proceso
- 🎯 **Cálculo automático**: Determina el número óptimo de frames
- 🔧 **Altamente configurable**: Control total sobre dimensiones, calidad y cantidad
- 💪 **Robusto**: Manejo profesional de errores y validaciones

## 📋 Requisitos

### Python 3.7+
Asegúrate de tener Python instalado:
```bash
python --version
```

### Librerías
Instala las dependencias usando pip:

```bash
pip install opencv-python numpy
```

O usando el archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Modo automático (recomendado):
```bash
python main.py video.mp4
```
Extrae automáticamente el número óptimo de frames (20 fps).

### Ver información del video:
```bash
python main.py video.mp4 --info
```

### Extraer número específico de frames:
```bash
python main.py video.mp4 -n 100
```

### Personalizar dimensiones:
```bash
python main.py video.mp4 -n 50 -w 1920 -h 1080
```

### Control de calidad:
```bash
python main.py video.mp4 -q 100
```
Calidad JPEG de 0 a 100 (mayor = mejor calidad, mayor tamaño).

### Configuración completa:
```bash
python main.py video.mp4 \
  -n 200 \
  -w 1920 \
  -h 1080 \
  -o mi_directorio \
  -q 95 \
  --fps 30
```

## 🎛️ Opciones disponibles

| Opción | Descripción | Default |
|--------|-------------|---------|
| `-n, --num-frames <N>` | Número de frames a extraer | Automático |
| `-w, --width <px>` | Ancho en pixels | 1200 |
| `-h, --height <px>` | Alto en pixels | 680 |
| `-o, --output <dir>` | Directorio de salida | `frames_output` |
| `-q, --quality <0-100>` | Calidad JPEG | 95 |
| `--fps <N>` | FPS para cálculo automático | 20 |
| `--info` | Solo mostrar info del video | - |
| `--help` | Mostrar ayuda | - |

## 📊 Ejemplo de salida

```
============================================================
📹 INFORMACIÓN DEL VIDEO
============================================================
📁 Archivo: mi_video.mp4
⏱️  Duración: 2m 30.0s
🎞️  FPS: 30.00
📊 Frames totales: 4,500
📐 Resolución: 1920x1080
============================================================

💡 Número óptimo calculado: 3000 frames
   (basado en 20 fps)

🎬 Extrayendo 3000 frames del video...
📁 Guardando en: frames_output
📐 Dimensiones: 1200x680
🎨 Calidad JPEG: 95%

──────────────────────────────────────────────────
📊 Progreso: [████████████████████████████████████████] 100.0% (3000/3000)
──────────────────────────────────────────────────

✅ Extracción completada!
📊 Frames extraídos exitosamente: 3000/3000

✨ Proceso completado exitosamente!
📂 Los frames están en: ./frames_output/
📝 Archivos creados: 3000

📋 Ejemplos de archivos creados:
   • frame000000.jpg
   • frame000001.jpg
   • frame000002.jpg
   ... y 2997 más
```

## 🧠 Conceptos técnicos explicados

### 1. OpenCV (cv2)
**OpenCV** (Open Source Computer Vision Library) es la librería más popular para visión por computadora.

**Funcionalidades usadas:**
- `cv2.VideoCapture()`: Abre y lee videos
- `cv2.CAP_PROP_*`: Propiedades del video (FPS, resolución, etc.)
- `cv2.resize()`: Redimensionamiento con interpolación
- `cv2.imwrite()`: Guarda imágenes con compresión JPEG

### 2. NumPy
**NumPy** es fundamental para operaciones numéricas y manejo de arrays.

**Uso en este script:**
- `np.linspace()`: Genera índices espaciados uniformemente
- `np.zeros()`: Crea canvas negro para padding
- Arrays multidimensionales para representar imágenes RGB

### 3. Algoritmos de interpolación

El script usa `INTER_LANCZOS4` para redimensionamiento:
- **INTER_NEAREST**: Más rápido, menor calidad
- **INTER_LINEAR**: Balance velocidad/calidad
- **INTER_CUBIC**: Buena calidad, más lento
- **INTER_LANCZOS4**: Mejor calidad, más lento (usado aquí)

### 4. Context Managers (`with`)

```python
with VideoFrameExtractor(video_path) as extractor:
    # código
```

Los context managers (`__enter__` y `__exit__`) garantizan:
- Apertura automática del video
- Liberación de recursos al terminar
- Cierre correcto incluso si hay errores

### 5. Espaciado uniforme

```python
frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
```

Si un video tiene 1000 frames y quieres 100:
- Frame 0, 10, 20, 30, ..., 990
- Distribución uniforme en lugar de primeros 100 frames consecutivos

### 6. Aspect Ratio (Proporción de aspecto)

El script calcula:
```python
ratio = min(target_width / w, target_height / h)
```

Ejemplo: Video 1920x1080 → Target 1200x680
- Ratio horizontal: 1200/1920 = 0.625
- Ratio vertical: 680/1080 = 0.629
- Usa el menor (0.625) para que quepa completo
- Resultado: 1200x675 + padding negro de 2.5px arriba/abajo

## 🎓 Ventajas de esta versión vs FFmpeg

| Aspecto | OpenCV | FFmpeg |
|---------|---------|---------|
| **Instalación** | `pip install` | Instalación de binario del sistema |
| **Portabilidad** | 100% Python | Dependencia externa |
| **Control** | Control pixel a pixel | Limitado a filtros |
| **Progreso** | Barra en tiempo real | Difícil de implementar |
| **Integración** | Fácil integración en apps Python | Subprocess externo |
| **Velocidad** | Buena | Excelente (C optimizado) |
| **Aprendizaje** | Enseña procesamiento de imágenes | Caja negra |

## 🔧 Troubleshooting

### Error: `No module named 'cv2'`
**Solución:**
```bash
pip install opencv-python
```

### Error: "No se pudo abrir el video"
**Posibles causas:**
1. Archivo corrupto
2. Códec no soportado por OpenCV
3. Permisos de archivo

**Solución:**
- Verifica que el archivo se reproduce en VLC u otro reproductor
- Intenta con otro archivo de video
- Convierte a H.264: `ffmpeg -i input.mp4 -c:v libx264 output.mp4`

### Los frames se ven pixelados
**Solución:**
- Aumenta la calidad JPEG: `-q 100`
- Usa dimensiones más grandes: `-w 1920 -h 1080`

### Memoria insuficiente
**Solución:**
- Reduce el número de frames: `-n 50`
- Reduce las dimensiones: `-w 800 -h 600`

## 🔬 Ejercicios para mejorar tus habilidades

### Nivel Básico
1. Agrega una opción para exportar en PNG en lugar de JPG
2. Implementa un modo "dry-run" que solo muestre qué haría sin ejecutar
3. Agrega validación de formatos de video soportados

### Nivel Intermedio
4. Implementa extracción basada en timestamps (ej: frame en 1:30, 2:45, etc.)
5. Añade detección automática de escenas para extraer solo frames significativos
6. Crea un modo "thumbnail" que genere una imagen con todos los frames en mosaico

### Nivel Avanzado
7. Implementa procesamiento paralelo usando `multiprocessing`
8. Añade filtros de imagen (blanco y negro, blur, contraste)
9. Crea una GUI usando tkinter o PyQt
10. Implementa exportación a formatos adicionales (WebP, AVIF)

## 📚 Recursos adicionales

- [OpenCV Documentation](https://docs.opencv.org/)
- [NumPy User Guide](https://numpy.org/doc/stable/user/)
- [Digital Image Processing Fundamentals](https://en.wikipedia.org/wiki/Digital_image_processing)
- [Video Codecs Explained](https://en.wikipedia.org/wiki/Video_codec)

## 🆚 Comparación: Sin librerías vs Con librerías

| Característica | Sin librerías (FFmpeg) | Con librerías (OpenCV) |
|----------------|------------------------|------------------------|
| **Instalación** | Requiere FFmpeg del sistema | `pip install` |
| **Código** | Más simple, llama subprocess | Más complejo, control fino |
| **Velocidad** | Muy rápida (C nativo) | Rápida (Python + C) |
| **Flexibilidad** | Limitada a flags FFmpeg | Total control programático |
| **Educativo** | Menos conceptos | Muchos conceptos CV |
| **Portabilidad** | Requiere FFmpeg instalado | Solo Python packages |

## 💡 Tips de optimización

1. **Para videos largos**: Reduce FPS óptimo (`--fps 10`)
2. **Para calidad máxima**: Usa `-q 100` y dimensiones grandes
3. **Para web**: Usa `-q 85` y dimensiones moderadas (balance tamaño/calidad)
4. **Para thumbnails**: `-w 320 -h 180 -q 80`

## 📝 Licencia

Código libre para uso educativo y personal.

## 🤝 Contribuciones

¿Ideas para mejorar? ¡Experimenta y aprende!
