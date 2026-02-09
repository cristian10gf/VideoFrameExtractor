#!/usr/bin/env python3
"""
Video Frame Extractor CLI - Versión con librerías
Extrae frames de un video MP4 y los guarda como imágenes JPG usando OpenCV.
"""

import sys
import os
import argparse
from pathlib import Path

try:
    import cv2
    import numpy as np
except ImportError:
    print("❌ ERROR: Librerías requeridas no encontradas.", file=sys.stderr)
    print("\nPor favor instala las dependencias:", file=sys.stderr)
    print("  pip install opencv-python numpy", file=sys.stderr)
    print("\nO usando el archivo requirements.txt:", file=sys.stderr)
    print("  pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)


class VideoFrameExtractor:
    """Clase para extraer frames de videos."""

    def __init__(self, video_path):
        """
        Inicializa el extractor con un archivo de video.

        Args:
            video_path: Ruta al archivo de video
        """
        self.video_path = video_path
        self.cap: cv2.VideoCapture
        self.video_info = {}

    def __enter__(self):
        """Context manager para manejar el video automáticamente."""
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise ValueError(f"No se pudo abrir el video: {self.video_path}")
        self._load_video_info()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Libera recursos al salir del context manager."""
        if self.cap:
            self.cap.release()

    def _load_video_info(self):
        """Carga información del video."""
        self.video_info = {
            'fps': self.cap.get(cv2.CAP_PROP_FPS),
            'total_frames': int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'duration': 0
        }

        if self.video_info['fps'] > 0:
            self.video_info['duration'] = self.video_info['total_frames'] / self.video_info['fps']

    def get_video_info(self):
        """Retorna información del video."""
        return self.video_info.copy()

    def calculate_optimal_frames(self, frames_per_second=20):
        """
        Calcula el número óptimo de frames a extraer.

        Args:
            frames_per_second: Frames deseados por segundo de video

        Returns:
            Número óptimo de frames
        """
        duration = self.video_info['duration']
        optimal = int(duration * frames_per_second)
        return max(1, min(optimal, self.video_info['total_frames']))

    def extract_frames(self, output_dir, num_frames=None, width=1200, height=680,
                      frames_per_second=20, quality=95):
        """
        Extrae frames del video espaciados uniformemente.

        Args:
            output_dir: Directorio donde guardar los frames
            num_frames: Número de frames a extraer (None para automático)
            width: Ancho de las imágenes resultantes
            height: Alto de las imágenes resultantes
            frames_per_second: FPS para cálculo automático
            quality: Calidad JPEG (0-100, mayor = mejor)

        Returns:
            Lista de rutas de archivos creados
        """
        # Crear directorio de salida
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Calcular número de frames si no se especificó
        if num_frames is None:
            num_frames = self.calculate_optimal_frames(frames_per_second)

        # Validar que no se pidan más frames de los disponibles
        num_frames = min(num_frames, self.video_info['total_frames'])

        # Calcular índices de frames a extraer (espaciados uniformemente)
        total_frames = self.video_info['total_frames']
        if num_frames == 1:
            frame_indices = [total_frames // 2]  # Frame del medio
        else:
            frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)

        print(f"\n🎬 Extrayendo {num_frames} frames del video...")
        print(f"📁 Guardando en: {output_dir}")
        print(f"📐 Dimensiones: {width}x{height}")
        print(f"🎨 Calidad JPEG: {quality}%")
        print(f"\n{'━' * 50}")

        extracted_files = []
        successful_extractions = 0

        # Parámetros de compresión JPEG
        jpeg_params = [cv2.IMWRITE_JPEG_QUALITY, quality]

        for idx, frame_number in enumerate(frame_indices):
            # Posicionar en el frame específico
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = self.cap.read()

            if not ret:
                print(f"⚠️  Advertencia: No se pudo leer frame {frame_number}", file=sys.stderr)
                continue

            # Redimensionar manteniendo aspecto
            resized_frame = self._resize_with_aspect_ratio(frame, width, height)

            # Generar nombre de archivo
            filename = f"frame{idx:06d}.jpg"
            filepath = os.path.join(output_dir, filename)

            # Guardar imagen
            success = cv2.imwrite(filepath, resized_frame, jpeg_params)

            if success:
                extracted_files.append(filepath)
                successful_extractions += 1

                # Mostrar progreso
                progress = (idx + 1) / len(frame_indices) * 100
                bar_length = 40
                filled = int(bar_length * (idx + 1) / len(frame_indices))
                bar = '█' * filled + '░' * (bar_length - filled)

                print(f"\r📊 Progreso: [{bar}] {progress:.1f}% ({idx + 1}/{len(frame_indices)})",
                      end='', flush=True)
            else:
                print(f"\n⚠️  Advertencia: No se pudo guardar {filename}", file=sys.stderr)

        print()  # Nueva línea después de la barra de progreso
        print(f"{'━' * 50}")
        print("\n✅ Extracción completada!")
        print(f"📊 Frames extraídos exitosamente: {successful_extractions}/{num_frames}")

        return extracted_files

    def _resize_with_aspect_ratio(self, image, target_width, target_height):
        """
        Redimensiona la imagen manteniendo la proporción y añadiendo padding si es necesario.

        Args:
            image: Imagen numpy array
            target_width: Ancho objetivo
            target_height: Alto objetivo

        Returns:
            Imagen redimensionada con padding
        """
        h, w = image.shape[:2]

        # Calcular ratio para mantener aspecto
        ratio = min(target_width / w, target_height / h)
        new_w = int(w * ratio)
        new_h = int(h * ratio)

        # Redimensionar
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

        # Crear imagen con padding negro
        canvas = np.zeros((target_height, target_width, 3), dtype=np.uint8)

        # Centrar la imagen redimensionada
        y_offset = (target_height - new_h) // 2
        x_offset = (target_width - new_w) // 2
        canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized

        return canvas


def parse_arguments():
    """Parsea los argumentos de línea de comandos usando argparse."""
    parser = argparse.ArgumentParser(
        description="Video Frame Extractor CLI - Extrae frames de un video usando OpenCV.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="""
Ejemplos:
    python main.py video.mp4
    python main.py video.mp4 -n 100
    python main.py video.mp4 -n 50 -w 1920 -h 1080 -q 100
    python main.py video.mp4 --info
        """
    )

    parser.add_argument("video_path", help="Ruta al archivo de video")
    parser.add_argument("-n", "--num-frames", type=int, default=None, help="Número de frames a extraer (auto si se omite)")
    parser.add_argument("-w", "--width", type=int, default=1200, help="Ancho de las imágenes")
    parser.add_argument("-h", "--height", type=int, default=680, help="Alto de las imágenes")
    parser.add_argument("-o", "--output", dest="output_dir", default="frames_output", help="Directorio de salida")
    parser.add_argument("-q", "--quality", type=int, default=95, help="Calidad JPEG (0-100)")
    parser.add_argument("--fps", dest="fps_for_optimal", type=float, default=20.0, help="FPS para cálculo óptimo")
    parser.add_argument("--info", dest="info_only", action="store_true", help="Solo muestra información del video")

    return vars(parser.parse_args())


def format_time(seconds):
    """Formatea segundos a formato legible."""
    minutes = int(seconds // 60)
    secs = seconds % 60
    if minutes > 0:
        return f"{minutes}m {secs:.1f}s"
    return f"{secs:.1f}s"


def format_size(width, height):
    """Formatea dimensiones."""
    return f"{width}x{height}"


def main():
    """Función principal del script."""
    # Parsear argumentos
    config = parse_arguments()

    # Verificar que el archivo existe
    if not os.path.isfile(config['video_path']):
        print(f"❌ Error: El archivo '{config['video_path']}' no existe", file=sys.stderr)
        sys.exit(1)

    try:
        # Abrir video y extraer información
        with VideoFrameExtractor(config['video_path']) as extractor:
            video_info = extractor.get_video_info()

            # Mostrar información del video
            print("\n" + "=" * 60)
            print("📹 INFORMACIÓN DEL VIDEO")
            print("=" * 60)
            print(f"📁 Archivo: {os.path.basename(config['video_path'])}")
            print(f"⏱️  Duración: {format_time(video_info['duration'])}")
            print(f"🎞️  FPS: {video_info['fps']:.2f}")
            print(f"📊 Frames totales: {video_info['total_frames']:,}")
            print(f"📐 Resolución: {format_size(video_info['width'], video_info['height'])}")
            print("=" * 60)

            # Si solo se pidió información, terminar aquí
            if config['info_only']:
                print("\nℹ️  Modo solo información activado. No se extrajeron frames.")
                sys.exit(0)

            # Calcular frames óptimos si no se especificó
            if config['num_frames'] is None:
                config['num_frames'] = extractor.calculate_optimal_frames(
                    config['fps_for_optimal']
                )
                print(f"\n💡 Número óptimo calculado: {config['num_frames']} frames")
                print(f"   (basado en {config['fps_for_optimal']} fps)")
            else:
                optimal = extractor.calculate_optimal_frames(config['fps_for_optimal'])
                print(f"\n💡 Frames solicitados: {config['num_frames']}")
                print(f"   (Valor óptimo sugerido: {optimal} frames)")

            # Extraer frames
            extracted_files = extractor.extract_frames(
                output_dir=config['output_dir'],
                num_frames=config['num_frames'],
                width=config['width'],
                height=config['height'],
                frames_per_second=config['fps_for_optimal'],
                quality=config['quality']
            )

            if extracted_files:
                print("\n✨ Proceso completado exitosamente!")
                print(f"📂 Los frames están en: ./{config['output_dir']}/")
                print(f"📝 Archivos creados: {len(extracted_files)}")

                # Mostrar algunos ejemplos
                print("\n📋 Ejemplos de archivos creados:")
                for filepath in extracted_files[:3]:
                    print(f"   • {os.path.basename(filepath)}")
                if len(extracted_files) > 3:
                    print(f"   ... y {len(extracted_files) - 3} más")

                sys.exit(0)
            else:
                print("\n❌ No se pudo extraer ningún frame", file=sys.stderr)
                sys.exit(1)

    except ValueError as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
