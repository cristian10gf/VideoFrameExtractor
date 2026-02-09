# Video Frame Extractor CLI v2 - Alto Rendimiento 🎬

Script CLI profesional en Python para extraer frames de videos de forma ultrarrápida usando **Decord**, **Typer**, **Rich** y **Pillow**.

## 🌟 Características

- ⚡ **Alto Rendimiento**: Decodificación hasta 3x más rápida gracias a `Decord`.
- ✨ **Extracción inteligente**: Frames espaciados uniformemente (no consecutivos).
- 🎨 **Redimensionamiento avanzado**: Mantiene proporción con padding automático (LANCZOS).
- 📊 **UI Moderna**: Barra de progreso profesional y tablas informativas con `Rich`.
- 🎯 **Cálculo automático**: Determina el número óptimo de frames basado en la duración.
- 🖼️ **Multi-formato**: Soporte nativo para JPG, PNG y WebP.
- 🔧 **Interfaz Typer**: CLI moderna con ayuda integrada y validación de tipos.

## 📋 Requisitos

### Python 3.12+
Asegúrate de tener una versión reciente de Python instalada.

### Librerías
Este proyecto utiliza `uv` para la gestión de dependencias, pero puedes instalarlas manualmente:

```bash
pip install decord numpy typer[all] Pillow rich
```

## 🚀 Uso

### Modo automático (recomendado):
```bash
python main.py video.mp4
```
Extrae automáticamente el número óptimo de frames (basado en 20 fps).

### Ver información profesional del video:
```bash
python main.py video.mp4 --info
```

### Exportar en formato WebP (más ligero):
```bash
python main.py video.mp4 -f webp
```

### Extraer número específico de frames:
```bash
python main.py video.mp4 -n 100
```

### Personalizar dimensiones:
```bash
python main.py video.mp4 -w 1920 -H 1080
```
*Nota: Se usa `-H` (mayúscula) para el alto para no entrar en conflicto con la ayuda (`-h`).*

### Configuración completa:
```bash
python main.py video.mp4 \
  -n 200 \
  -w 1920 \
  -H 1080 \
  -o mi_directorio \
  -q 95 \
  -f png
```

## 🎛️ Opciones disponibles

| Opción | Descripción | Default |
|--------|-------------|---------|
| `VIDEO` | Ruta al archivo de video (Argumento) | Requerido |
| `-n, --num-frames <N>` | Número de frames a extraer | Automático |
| `-w, --width <px>` | Ancho en píxeles | 1200 |
| `-H, --height <px>` | Alto en píxeles | 680 |
| `-o, --output <dir>` | Directorio de salida | `frames_output` |
| `-q, --quality <0-100>` | Calidad de imagen | 95 |
| `-f, --format <ext>` | Formato: `jpg`, `png`, `webp` | `jpg` |
| `--fps <N>` | FPS para cálculo automático | 20.0 |
| `--info` | Solo mostrar info del video | - |
| `--help` | Mostrar ayuda | - |

## 🧠 Conceptos técnicos clave

### 1. Decord
Utilizado para la decodificación de video. A diferencia de OpenCV, Decord está diseñado para entrenamiento de Deep Learning y es significativamente más eficiente en el acceso aleatorio a frames.

### 2. Pillow (PIL)
Se encarga del redimensionamiento de alta calidad (LANCZOS) y del guardado de imágenes en formatos modernos como WebP.

### 3. Rich
Proporciona la interfaz visual, incluyendo la barra de progreso con estimación de tiempo restante y tablas formateadas para los metadatos del video.

## 🎓 Ventajas de la v2 vs OpenCV Tradicional

| Aspecto | Versión Actual (v2) | Versión OpenCV |
|---------|---------------------|----------------|
| **Velocidad** | ⚡ Ultrarrápida | Estándar |
| **Formatos** | JPG, PNG, WebP | Limitado |
| **CLI** | Typer (Moderna) | argparse (Básica) |
| **Feedback** | Barra de progreso con ETA | Porcentaje simple |
| **Código** | Más conciso y legible | Verboso |

## 📝 Licencia

Código libre para uso educativo y personal.
