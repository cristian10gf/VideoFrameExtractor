# 🎓 Guía Teórica: Procesamiento de Video e Imágenes con Python

## 📚 Tabla de Contenidos

1. [Conceptos Fundamentales](#conceptos-fundamentales)
2. [Representación Digital de Imágenes](#representación-digital-de-imágenes)
3. [Formatos de Video](#formatos-de-video)
4. [OpenCV en Profundidad](#opencv-en-profundidad)
5. [Algoritmos de Redimensionamiento](#algoritmos-de-redimensionamiento)
6. [Compresión JPEG](#compresión-jpeg)
7. [Best Practices](#best-practices)

---

## 1. Conceptos Fundamentales

### ¿Qué es un video digital?

Un video digital es una **secuencia de imágenes estáticas** (frames) mostradas rápidamente para crear la ilusión de movimiento.

**Componentes clave:**
- **Frame**: Una imagen individual
- **FPS (Frames Per Second)**: Cuadros por segundo
  - Cine: 24 fps
  - TV/Video: 30 fps (NTSC) o 25 fps (PAL)
  - Videojuegos: 60+ fps
  - Video profesional: 120+ fps

**Cálculo básico:**
```
Duración (segundos) = Total de frames / FPS
Total de frames = Duración × FPS

Ejemplo: Video de 2 minutos a 30 fps
Total frames = 120 segundos × 30 fps = 3,600 frames
```

### ¿Qué es un pixel?

Un **pixel** (picture element) es la unidad más pequeña de una imagen digital.

**Representación de color RGB:**
```
Pixel = (R, G, B)
donde:
  R = Red (Rojo): 0-255
  G = Green (Verde): 0-255
  B = Blue (Azul): 0-255
```

**Ejemplos:**
- Negro: (0, 0, 0)
- Blanco: (255, 255, 255)
- Rojo puro: (255, 0, 0)
- Amarillo: (255, 255, 0)

---

## 2. Representación Digital de Imágenes

### Arrays NumPy

En Python con OpenCV y NumPy, una imagen es un **array tridimensional**:

```python
import numpy as np
import cv2

# Crear imagen de 100x100 pixels en negro
imagen = np.zeros((100, 100, 3), dtype=np.uint8)

# Forma del array
print(imagen.shape)  # (100, 100, 3)
#                     altura, ancho, canales

# Modificar un pixel
imagen[50, 50] = [255, 0, 0]  # Pixel rojo en el centro
```

**Estructura:**
```
imagen[y, x, c]

y = coordenada vertical (fila)
x = coordenada horizontal (columna)
c = canal de color (0=B, 1=G, 2=R)

⚠️ IMPORTANTE: OpenCV usa BGR, no RGB
```

### Tipos de datos

```python
# uint8: 0-255 (estándar para imágenes)
imagen_8bit = np.zeros((100, 100, 3), dtype=np.uint8)

# float32: 0.0-1.0 (útil para procesamiento)
imagen_float = imagen_8bit.astype(np.float32) / 255.0

# Convertir de vuelta
imagen_8bit = (imagen_float * 255).astype(np.uint8)
```

---

## 3. Formatos de Video

### Contenedores vs Códecs

**Contenedor** (Container):
- Formato del archivo: `.mp4`, `.avi`, `.mkv`, `.mov`
- Encapsula video, audio, subtítulos, metadata

**Códec** (Codec = Compressor/Decompressor):
- Algoritmo de compresión/descompresión
- Video: H.264, H.265 (HEVC), VP9, AV1
- Audio: AAC, MP3, Opus

**Ejemplo:**
```
archivo.mp4
├── Video (códec H.264)
├── Audio (códec AAC)
└── Metadata (duración, FPS, etc.)
```

### Códecs populares

| Códec | Pros | Contras | Uso |
|-------|------|---------|-----|
| **H.264** | Universal, buena compresión | Patentado | YouTube, streaming |
| **H.265** | Mejor compresión que H.264 | Requiere más CPU | 4K, HDR |
| **VP9** | Libre, buena compresión | Lento de encodear | YouTube, web |
| **AV1** | Mejor compresión, libre | Muy lento | Futuro del streaming |

---

## 4. OpenCV en Profundidad

### VideoCapture

```python
import cv2

# Abrir video
cap = cv2.VideoCapture('video.mp4')

# Verificar si se abrió correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir el video")
    exit()

# Obtener propiedades
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"FPS: {fps}")
print(f"Resolución: {width}x{height}")
print(f"Total frames: {total_frames}")

# Leer frame por frame
while True:
    ret, frame = cap.read()
    
    if not ret:
        break  # No hay más frames
    
    # Procesar frame aquí
    # frame es un numpy array de shape (height, width, 3)
    
# Liberar recursos
cap.release()
```

### Propiedades útiles de VideoCapture

```python
# CAP_PROP_FPS: Frames por segundo
fps = cap.get(cv2.CAP_PROP_FPS)

# CAP_PROP_FRAME_COUNT: Total de frames
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# CAP_PROP_FRAME_WIDTH/HEIGHT: Dimensiones
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# CAP_PROP_POS_FRAMES: Frame actual
current = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

# Saltar a frame específico
cap.set(cv2.CAP_PROP_POS_FRAMES, 100)
ret, frame = cap.read()  # Lee el frame 100
```

---

## 5. Algoritmos de Redimensionamiento

### Métodos de interpolación

Cuando redimensionas una imagen, necesitas "inventar" pixels nuevos. Esto se llama **interpolación**.

#### 1. INTER_NEAREST (Vecino más cercano)
```python
resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
```
- **Más rápido**
- **Menor calidad**: Produce efectos de "pixelación"
- **Uso**: Cuando la velocidad es crítica

#### 2. INTER_LINEAR (Bilinear)
```python
resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
```
- **Balance velocidad/calidad**
- Promedia los 4 pixels vecinos más cercanos
- **Uso**: Redimensionamiento general

#### 3. INTER_CUBIC (Bicúbic)
```python
resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
```
- **Buena calidad**
- Usa 16 pixels vecinos
- Más lento que bilinear
- **Uso**: Cuando necesitas mejor calidad

#### 4. INTER_LANCZOS4 (Lanczos)
```python
resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
```
- **Mejor calidad**
- Usa ventana de 8x8 pixels
- **Más lento**
- **Uso**: Mejor calidad posible (usado en nuestro script)

### Visualización de diferencias

```
Original: 1920x1080

INTER_NEAREST:    [■][■][■]  <- Blocky, bordes duros
                  [■][■][■]

INTER_LINEAR:     [▓][▓][▓]  <- Suave, puede perder detalle
                  [▓][▓][▓]

INTER_LANCZOS4:   [▒][▒][▒]  <- Muy suave, preserva detalles
                  [▒][▒][▒]
```

### Aspect Ratio (Proporción de aspecto)

**Problema:** Si cambias width y height independientemente, la imagen se distorsiona.

**Solución:** Calcular el ratio y usar padding.

```python
def resize_with_aspect_ratio(image, target_w, target_h):
    h, w = image.shape[:2]
    
    # Calcular ratio para que la imagen quepa
    ratio = min(target_w / w, target_h / h)
    
    # Nuevas dimensiones
    new_w = int(w * ratio)
    new_h = int(h * ratio)
    
    # Redimensionar
    resized = cv2.resize(image, (new_w, new_h))
    
    # Crear canvas negro
    canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
    
    # Centrar imagen
    y_offset = (target_h - new_h) // 2
    x_offset = (target_w - new_w) // 2
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    
    return canvas
```

**Ejemplo:**
```
Video original: 1920x1080 (16:9)
Target: 1200x1200 (1:1)

Sin preservar aspecto:
[████████████████]  <- Distorsionado

Con aspecto preservado:
[                ]
[████████████████]  <- Centrado con padding
[                ]
```

---

## 6. Compresión JPEG

### ¿Cómo funciona JPEG?

JPEG es un formato de **compresión con pérdida** para imágenes.

**Proceso simplificado:**
1. **Conversión de espacio de color**: RGB → YCbCr
   - Y: Luminancia (brillo)
   - Cb/Cr: Crominancia (color)
   
2. **Submuestreo de crominancia**: Reduce resolución de color
   - El ojo humano es más sensible al brillo que al color
   
3. **DCT (Discrete Cosine Transform)**: Convierte bloques 8x8 a frecuencias

4. **Cuantización**: Descarta información menos importante
   - Aquí es donde se pierde calidad
   
5. **Codificación**: Comprime los datos

### Parámetro de calidad

```python
# Calidad JPEG en OpenCV: 0-100
cv2.imwrite('imagen.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 95])
```

**Efectos de la calidad:**

| Calidad | Tamaño | Uso |
|---------|--------|-----|
| 100 | ~5 MB | Archivado, edición |
| 95 | ~2 MB | Fotografía profesional |
| 85 | ~800 KB | Web de alta calidad |
| 75 | ~400 KB | Web estándar |
| 60 | ~200 KB | Redes sociales |
| 50 | ~150 KB | Thumbnails |

**Artefactos de compresión:**
```
Calidad 100:  ░░▒▒▓▓  <- Suave, sin bloques
Calidad 50:   ██▓▓░░  <- Bloques visibles 8x8
Calidad 10:   ██████  <- Muy bloqueado
```

---

## 7. Best Practices

### Performance

```python
# ❌ MAL: Leer todo el video en memoria
frames = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)  # Consumirá mucha RAM

# ✅ BIEN: Procesar frame por frame
while True:
    ret, frame = cap.read()
    if not ret:
        break
    process_and_save(frame)  # Procesa y descarta
```

### Manejo de recursos

```python
# ❌ MAL: Sin liberar recursos
cap = cv2.VideoCapture('video.mp4')
# ... código ...
# Si hay error, cap nunca se cierra

# ✅ BIEN: Usar context manager
class VideoCapture:
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
    
    def __enter__(self):
        return self.cap
    
    def __exit__(self, *args):
        self.cap.release()

with VideoCapture('video.mp4') as cap:
    # Código
    pass
# Automáticamente se libera
```

### Validación de entrada

```python
# ✅ BIEN: Validar antes de procesar
def process_video(video_path):
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video no existe: {video_path}")
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"No se pudo abrir: {video_path}")
    
    # Verificar que tiene frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        raise ValueError("Video sin frames")
    
    # Procesar...
```

### Espaciado de frames

```python
# ❌ MAL: Frames consecutivos
for i in range(100):
    ret, frame = cap.read()
    save_frame(frame, i)
# Solo extrae los primeros 100 frames

# ✅ BIEN: Frames espaciados uniformemente
import numpy as np

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
indices = np.linspace(0, total_frames-1, 100, dtype=int)

for i, frame_idx in enumerate(indices):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    save_frame(frame, i)
# Extrae 100 frames distribuidos en todo el video
```

---

## 🎯 Ejercicios Prácticos

### Nivel 1: Básico

1. **Leer y mostrar información de un video**
   - Abre un video con OpenCV
   - Muestra: duración, FPS, resolución, total de frames

2. **Extraer el frame del medio**
   - Calcula qué frame está en la mitad del video
   - Guárdalo como imagen

3. **Crear un mosaico**
   - Extrae 4 frames espaciados
   - Combínalos en una imagen 2x2

### Nivel 2: Intermedio

4. **Comparar métodos de interpolación**
   - Redimensiona la misma imagen con los 4 métodos
   - Guarda y compara visualmente

5. **Comparar calidades JPEG**
   - Guarda la misma imagen con calidades 100, 75, 50, 25
   - Compara tamaños de archivo y calidad visual

6. **Extractor con histograma**
   - Extrae frames
   - Para cada frame, calcula y guarda su histograma de colores

### Nivel 3: Avanzado

7. **Detección de cambios de escena**
   - Compara frames consecutivos
   - Detecta cuándo hay cambio significativo
   - Solo guarda frames en cambios de escena

8. **Procesamiento paralelo**
   - Usa `multiprocessing` para procesar múltiples frames simultáneamente

9. **Generador de timelapse**
   - Toma frames espaciados de un video largo
   - Genera un nuevo video acelerado

---

## 📖 Recursos Adicionales

### Documentación
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [NumPy Documentation](https://numpy.org/doc/stable/)
- [Digital Image Processing - Gonzalez & Woods](https://www.imageprocessingplace.com/)

### Conceptos Avanzados
- **Color Spaces**: RGB, HSV, LAB, YCbCr
- **Filtros**: Blur, Sharpen, Edge Detection
- **Transformaciones**: Rotación, Perspectiva, Affine
- **Machine Learning**: Object Detection, Segmentation

### Herramientas
- **FFmpeg**: Procesamiento avanzado de video
- **ImageMagick**: Procesamiento de imágenes
- **Pillow**: Alternativa a OpenCV para imágenes
- **scikit-image**: Algoritmos científicos de procesamiento

---

## 💡 Conclusión

El procesamiento de video e imágenes combina:
- **Matemáticas**: Álgebra lineal, transformadas, estadística
- **Programación**: Algoritmos eficientes, manejo de memoria
- **Teoría**: Compresión, percepción visual, espacios de color

**Próximos pasos para aprender:**
1. Experimenta con diferentes parámetros
2. Lee la documentación de OpenCV
3. Implementa tus propios filtros y transformaciones
4. Explora Computer Vision con Deep Learning

¡Sigue practicando! 🚀
