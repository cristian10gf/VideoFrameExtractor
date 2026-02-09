#!/usr/bin/env python3
"""
Video Frame Extractor CLI v2 - Alto rendimiento con Decord, Typer y Rich.
Extrae frames de videos de forma rápida y eficiente.
"""

from pathlib import Path
from typing import Optional
from enum import Enum

import numpy as np
import typer
from decord import VideoReader, cpu
from PIL import Image
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
)
from rich.table import Table

app = typer.Typer(
    name="videoframeextractor",
    help="CLI de alto rendimiento para extraer frames de videos.",
    add_completion=True,
)
console = Console()


class ImageFormat(str, Enum):
    """Formatos de imagen soportados."""
    jpg = "jpg"
    png = "png"
    webp = "webp"


class VideoFrameExtractor:
    """Extractor de frames de video usando Decord (2-3x más rápido que OpenCV)."""

    def __init__(self, video_path: str):
        self.video_path = video_path
        self.vr = VideoReader(video_path, ctx=cpu(0))
        self.fps = self.vr.get_avg_fps()
        self.total_frames = len(self.vr)
        self.width, self.height = self.vr[0].shape[1], self.vr[0].shape[0]
        self.duration = self.total_frames / self.fps if self.fps > 0 else 0

    def get_info(self) -> dict:
        """Retorna metadatos del video."""
        return {
            "fps": self.fps,
            "total_frames": self.total_frames,
            "width": self.width,
            "height": self.height,
            "duration": self.duration,
        }

    def calculate_optimal_frames(self, target_fps: float = 20.0) -> int:
        """Calcula frames óptimos basado en FPS objetivo."""
        optimal = int(self.duration * target_fps)
        return max(1, min(optimal, self.total_frames))

    def extract_frames(
        self,
        output_dir: Path,
        num_frames: Optional[int],
        width: int,
        height: int,
        quality: int,
        target_fps: float,
        fmt: ImageFormat,
    ) -> list[Path]:
        """Extrae frames espaciados uniformemente usando batch loading."""
        output_dir.mkdir(parents=True, exist_ok=True)

        if num_frames is None:
            num_frames = self.calculate_optimal_frames(target_fps)
        num_frames = min(num_frames, self.total_frames)

        # Índices espaciados uniformemente
        if num_frames == 1:
            indices = [self.total_frames // 2]
        else:
            indices = np.linspace(0, self.total_frames - 1, num_frames, dtype=int).tolist()

        extracted = []
        extension = fmt.value

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            MofNCompleteColumn(),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Extrayendo frames...", total=len(indices))

            for idx, frame_idx in enumerate(indices):
                frame = self.vr[frame_idx].asnumpy()  # RGB numpy array
                resized = self._resize_with_padding(frame, width, height)

                # Convertir a PIL y guardar
                img = Image.fromarray(resized)
                filepath = output_dir / f"frame{idx:06d}.{extension}"

                save_params = self._get_save_params(fmt, quality)
                img.save(filepath, **save_params)

                extracted.append(filepath)
                progress.update(task, advance=1)

        return extracted

    def _resize_with_padding(self, image: np.ndarray, target_w: int, target_h: int) -> np.ndarray:
        """Redimensiona manteniendo aspecto con padding negro."""
        h, w = image.shape[:2]
        ratio = min(target_w / w, target_h / h)
        new_w, new_h = int(w * ratio), int(h * ratio)

        # Usar PIL para resize de alta calidad (LANCZOS)
        pil_img = Image.fromarray(image)
        resized = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # Crear canvas con padding
        canvas = Image.new("RGB", (target_w, target_h), (0, 0, 0))
        x_offset = (target_w - new_w) // 2
        y_offset = (target_h - new_h) // 2
        canvas.paste(resized, (x_offset, y_offset))

        return np.array(canvas)

    @staticmethod
    def _get_save_params(fmt: ImageFormat, quality: int) -> dict:
        """Retorna parámetros de guardado según formato."""
        if fmt == ImageFormat.jpg:
            return {"format": "JPEG", "quality": quality}
        elif fmt == ImageFormat.png:
            compress = max(0, min(9, (100 - quality) // 10))
            return {"format": "PNG", "compress_level": compress}
        elif fmt == ImageFormat.webp:
            return {"format": "WEBP", "quality": quality}
        return {}


def format_duration(seconds: float) -> str:
    """Formatea duración en formato legible."""
    mins, secs = divmod(seconds, 60)
    return f"{int(mins)}m {secs:.1f}s" if mins else f"{secs:.1f}s"


def show_video_info(extractor: VideoFrameExtractor, filename: str) -> None:
    """Muestra información del video en tabla Rich."""
    info = extractor.get_info()

    table = Table(title="Información del Video", show_header=False, border_style="blue")
    table.add_column("Campo", style="cyan")
    table.add_column("Valor", style="green")

    table.add_row("Archivo", filename)
    table.add_row("Duración", format_duration(info["duration"]))
    table.add_row("FPS", f"{info['fps']:.2f}")
    table.add_row("Frames totales", f"{info['total_frames']:,}")
    table.add_row("Resolución", f"{info['width']}x{info['height']}")

    console.print(table)


@app.command()
def extract(
    video: Path = typer.Argument(..., help="Ruta al archivo de video", exists=True),
    num_frames: Optional[int] = typer.Option(None, "-n", "--num-frames", help="Número de frames (auto si se omite)"),
    width: int = typer.Option(1200, "-w", "--width", help="Ancho de las imágenes"),
    height: int = typer.Option(680, "-H", "--height", help="Alto de las imágenes"),
    output: Path = typer.Option(Path("frames_output"), "-o", "--output", help="Directorio de salida"),
    quality: int = typer.Option(95, "-q", "--quality", min=0, max=100, help="Calidad (0-100)"),
    fps: float = typer.Option(20.0, "--fps", help="FPS para cálculo automático"),
    fmt: ImageFormat = typer.Option(ImageFormat.jpg, "-f", "--format", help="Formato de imagen"),
    info_only: bool = typer.Option(False, "--info", help="Solo mostrar información del video"),
) -> None:
    """Extrae frames de un video de forma rápida y eficiente."""
    try:
        with console.status("[bold blue]Abriendo video y analizando frames...", spinner="dots"):
            extractor = VideoFrameExtractor(str(video))
    except Exception as e:
        console.print(f"[red]Error al abrir el video:[/red] {e}")
        raise typer.Exit(1)

    show_video_info(extractor, video.name)

    if info_only:
        console.print("\n[yellow]Modo información: no se extrajeron frames.[/yellow]")
        raise typer.Exit(0)

    # Mostrar configuración
    actual_frames = num_frames or extractor.calculate_optimal_frames(fps)
    console.print("\n[bold]Configuración:[/bold]")
    console.print(f"  Frames a extraer: [cyan]{actual_frames}[/cyan]")
    console.print(f"  Dimensiones: [cyan]{width}x{height}[/cyan]")
    console.print(f"  Formato: [cyan]{fmt.value.upper()}[/cyan] (calidad: {quality}%)")
    console.print(f"  Salida: [cyan]{output}[/cyan]\n")

    # Extraer
    extracted = extractor.extract_frames(
        output_dir=output,
        num_frames=num_frames,
        width=width,
        height=height,
        quality=quality,
        target_fps=fps,
        fmt=fmt,
    )

    if extracted:
        console.print(f"\n[green]Extracción completada:[/green] {len(extracted)} frames")
        console.print(f"[dim]Ubicación: {output.absolute()}[/dim]")

        # Mostrar ejemplos
        console.print("\n[bold]Archivos creados:[/bold]")
        for f in extracted[:3]:
            console.print(f"  [dim]{f.name}[/dim]")
        if len(extracted) > 3:
            console.print(f"  [dim]... y {len(extracted) - 3} más[/dim]")
    else:
        console.print("[red]No se pudo extraer ningún frame.[/red]")
        raise typer.Exit(1)


def main() -> None:
    """Punto de entrada principal."""
    app()


if __name__ == "__main__":
    main()

