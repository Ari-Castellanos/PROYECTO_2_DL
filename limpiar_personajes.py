#!/usr/bin/env python3
"""Audita y prepara imágenes RGB de 64x64 para una GAN, sin tocar originales.

Ejemplo: python limpiar_personajes.py --input /ruta/dataset --output ./datos_limpios
Dependencias: Pillow; opcional imagehash para detectar casi duplicados.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def arguments():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path, help="Directorio extraído de Kaggle")
    p.add_argument("--output", required=True, type=Path, help="Directorio de salida NUEVO")
    p.add_argument("--size", type=int, default=64)
    p.add_argument("--min-side", type=int, default=64)
    p.add_argument("--phash-distance", type=int, default=-1,
                   help="Distancia perceptual máxima para excluir casi duplicados; -1 desactiva, 0=hash igual")
    p.add_argument("--crop", choices=["center", "pad"], default="center",
                   help="center recorta a cuadrado; pad conserva la imagen completa")
    return p.parse_args()


def main():
    a = arguments()
    source = a.input.expanduser().resolve()
    dest = a.output.expanduser().resolve()
    if not source.is_dir() or a.size < 1 or a.min_side < 1:
        raise ValueError("Compruebe --input, --size y --min-side")
    if dest == source or source in dest.parents or dest in source.parents:
        raise ValueError("La salida debe estar fuera del directorio de entrada y viceversa")
    if dest.exists() and any(dest.iterdir()):
        raise FileExistsError(f"La salida ya contiene archivos: {dest}")
    if a.phash_distance < -1 or a.phash_distance > 64:
        raise ValueError("--phash-distance debe estar entre -1 y 64")
    if a.phash_distance >= 0:
        try:
            import imagehash
        except ImportError as exc:
            raise SystemExit("Instale imagehash: pip install imagehash") from exc

    files = sorted((p for p in source.rglob("*") if p.is_file() and p.suffix.lower() in EXTS),
                   key=lambda p: str(p.relative_to(source)).lower())
    dest.mkdir(parents=True, exist_ok=True)
    images_dir = dest / "images"
    images_dir.mkdir()
    rows, seen_pixels, seen_phashes = [], {}, []
    for path in files:
        relative = path.relative_to(source).as_posix()
        row = {"source": relative, "status": "", "reason": "", "output": "", "width": "", "height": ""}
        try:
            with Image.open(path) as original:
                original.load()  # Fuerza la decodificación; detecta truncamientos.
                im = ImageOps.exif_transpose(original)
                row["width"], row["height"] = im.size
                if min(im.size) < a.min_side:
                    row.update(status="excluded", reason="too_small")
                else:
                    if im.mode in ("RGBA", "LA") or "transparency" in im.info:
                        rgba = im.convert("RGBA")
                        bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
                        im = Image.alpha_composite(bg, rgba).convert("RGB")
                    else:
                        im = im.convert("RGB")
                    # Duplicados exactos por píxeles orientados: extensiones y compresión pueden variar.
                    digest = hashlib.sha256(im.width.to_bytes(4, "big") + im.height.to_bytes(4, "big") + im.tobytes()).hexdigest()
                    if digest in seen_pixels:
                        row.update(status="excluded", reason=f"exact_duplicate:{seen_pixels[digest]}")
                    else:
                        if a.crop == "center":
                            im = ImageOps.fit(im, (a.size, a.size), method=Image.Resampling.LANCZOS)
                        else:
                            im.thumbnail((a.size, a.size), Image.Resampling.LANCZOS)
                            canvas = Image.new("RGB", (a.size, a.size), (255, 255, 255))
                            canvas.paste(im, ((a.size - im.width) // 2, (a.size - im.height) // 2))
                            im = canvas
                        candidate = imagehash.phash(im) if a.phash_distance >= 0 else None
                        match = next((name for h, name in seen_phashes if candidate - h <= a.phash_distance), None) if candidate is not None else None
                        if match:
                            row.update(status="excluded", reason=f"near_duplicate:{match}")
                        else:
                            name = f"img_{len(seen_pixels):06d}.png"
                            im.save(images_dir / name)
                            row.update(status="kept", output=f"images/{name}")
                            seen_pixels[digest] = relative
                            if candidate is not None:
                                seen_phashes.append((candidate, relative))
        except (OSError, ValueError, UnidentifiedImageError, Image.DecompressionBombError) as exc:
            row.update(status="excluded", reason=f"unreadable:{type(exc).__name__}")
        rows.append(row)

    with (dest / "manifest.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "status", "reason", "output", "width", "height"])
        writer.writeheader()
        writer.writerows(rows)
    reasons = {}
    for row in rows:
        key = row["reason"].split(":", 1)[0] if row["reason"] else "kept"
        reasons[key] = reasons.get(key, 0) + 1
    report = {"input": str(source), "total_candidates": len(files), "counts": reasons,
              "output_size": a.size, "crop": a.crop, "min_side": a.min_side,
              "phash_distance": a.phash_distance,
              "note": "No detecta automáticamente escenas sin personajes ni resuelve permisos de uso. Revisar visualmente."}
    (dest / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
