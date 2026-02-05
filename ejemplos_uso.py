#!/usr/bin/env python3
"""
Ejemplos de uso del Video Frame Extractor
Este script muestra diferentes formas de usar el extractor de frames.
"""

import os
import sys

# Ejemplos de comandos que puedes ejecutar

EXAMPLES = [
    {
        "title": "Extracción Automática Básica",
        "description": "Extrae el número óptimo de frames con configuración por defecto",
        "command": "python video_frame_extractor_cv2.py mi_video.mp4"
    },
    {
        "title": "Solo Ver Información",
        "description": "Muestra información del video sin extraer frames",
        "command": "python video_frame_extractor_cv2.py mi_video.mp4 --info"
    },
    {
        "title": "Extracción Específica",
        "description": "Extrae exactamente 100 frames",
        "command": "python video_frame_extractor_cv2.py mi_video.mp4 -n 100"
    },
    {
        "title": "Alta Resolución",
        "description": "Extrae frames en resolución Full HD",
        "command": "python video_frame_extractor_cv2.py mi_video.mp4 -w 1920 -h 1080"
    },
    {
        "title": "Máxima Calidad",
        "description": "Extrae con calidad JPEG máxima (archivos más grandes)",
        "command": "python video_frame_extractor_cv2.py mi_video.mp4 -q 100"
    },
    {
        "title": "Thumbnails para Web",
        "description": "Genera thumbnails pequeños optimizados para web",
        "command": "python video_frame_extractor_cv2.py mi_video.mp4 -n 20 -w 320 -h 180 -q 80 -o thumbnails"
    },
    {
        "title": "Configuración Personalizada",
        "description": "Extrae 200 frames con configuración personalizada completa",
        "command": "python video_frame_extractor_cv2.py mi_video.mp4 -n 200 -w 1280 -h 720 -o mis_frames -q 95 --fps 25"
    },
    {
        "title": "Extracción Densa",
        "description": "Extrae muchos frames (30 por segundo de video)",
        "command": "python video_frame_extractor_cv2.py mi_video.mp4 --fps 30"
    },
    {
        "title": "Extracción Dispersa",
        "description": "Extrae pocos frames (5 por segundo de video)",
        "command": "python video_frame_extractor_cv2.py mi_video.mp4 --fps 5"
    },
    {
        "title": "Tamaño Instagram Story",
        "description": "Dimensiones para Instagram Stories (1080x1920)",
        "command": "python video_frame_extractor_cv2.py mi_video.mp4 -w 1080 -h 1920 -o instagram_frames"
    }
]


def print_examples():
    """Imprime todos los ejemplos de uso."""
    print("\n" + "=" * 70)
    print("  📚 EJEMPLOS DE USO - VIDEO FRAME EXTRACTOR")
    print("=" * 70 + "\n")
    
    for i, example in enumerate(EXAMPLES, 1):
        print(f"[{i}] {example['title']}")
        print(f"    {example['description']}")
        print(f"    \n    $ {example['command']}\n")
        print("-" * 70)
    
    print("\n💡 TIP: Reemplaza 'mi_video.mp4' con la ruta a tu archivo de video\n")


def interactive_mode():
    """Modo interactivo para generar comandos personalizados."""
    print("\n" + "=" * 70)
    print("  🎯 MODO INTERACTIVO - GENERADOR DE COMANDOS")
    print("=" * 70 + "\n")
    
    # Solicitar archivo de video
    video_file = input("📁 Ruta al archivo de video (ejemplo: video.mp4): ").strip()
    if not video_file:
        print("❌ Debe proporcionar un archivo de video")
        return
    
    # Número de frames
    print("\n¿Cuántos frames deseas extraer?")
    print("  [1] Automático (recomendado)")
    print("  [2] Número específico")
    num_choice = input("Opción (1-2): ").strip()
    
    num_frames_arg = ""
    if num_choice == "2":
        num_frames = input("Cantidad de frames: ").strip()
        if num_frames:
            num_frames_arg = f"-n {num_frames}"
    
    # Dimensiones
    print("\n¿Qué dimensiones deseas?")
    print("  [1] Por defecto (1200x680)")
    print("  [2] Full HD (1920x1080)")
    print("  [3] HD (1280x720)")
    print("  [4] Personalizado")
    dim_choice = input("Opción (1-4): ").strip()
    
    dimensions_arg = ""
    if dim_choice == "2":
        dimensions_arg = "-w 1920 -h 1080"
    elif dim_choice == "3":
        dimensions_arg = "-w 1280 -h 720"
    elif dim_choice == "4":
        width = input("Ancho (px): ").strip()
        height = input("Alto (px): ").strip()
        if width and height:
            dimensions_arg = f"-w {width} -h {height}"
    
    # Calidad
    print("\n¿Qué calidad JPEG deseas? (0-100)")
    print("  [1] Muy alta (95) - Recomendado")
    print("  [2] Alta (85)")
    print("  [3] Media (75)")
    print("  [4] Personalizada")
    quality_choice = input("Opción (1-4): ").strip()
    
    quality_arg = ""
    if quality_choice == "2":
        quality_arg = "-q 85"
    elif quality_choice == "3":
        quality_arg = "-q 75"
    elif quality_choice == "4":
        quality = input("Calidad (0-100): ").strip()
        if quality:
            quality_arg = f"-q {quality}"
    
    # Directorio de salida
    output_dir = input("\n📂 Directorio de salida (Enter para 'frames_output'): ").strip()
    output_arg = f"-o {output_dir}" if output_dir else ""
    
    # Construir comando
    command_parts = [
        "python video_frame_extractor_cv2.py",
        video_file,
        num_frames_arg,
        dimensions_arg,
        quality_arg,
        output_arg
    ]
    
    command = " ".join(filter(None, command_parts))
    
    print("\n" + "=" * 70)
    print("✨ COMANDO GENERADO:")
    print("=" * 70)
    print(f"\n{command}\n")
    print("=" * 70)
    
    # Preguntar si ejecutar
    run = input("\n¿Ejecutar este comando ahora? (s/n): ").strip().lower()
    if run == 's':
        print("\n🚀 Ejecutando...\n")
        os.system(command)
    else:
        print("\n💾 Copia el comando de arriba para ejecutarlo más tarde")


def main():
    """Función principal."""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        print_examples()
        print("\n🎯 Para modo interactivo, ejecuta:")
        print("   python ejemplos_uso.py --interactive\n")


if __name__ == '__main__':
    main()
