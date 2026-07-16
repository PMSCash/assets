#!/usr/bin/env python3
"""Build EJL-Lighthouse-all-images.pdf from drawings/ + images/."""
from __future__ import annotations

import re
import shutil
from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "download" / "EJL-Lighthouse-all-images.pdf"
OUT_COPY = ROOT / "EJL-Lighthouse-all-images.pdf"

PINK = (1.0, 0.176, 0.584)
GOLD = (0.831, 0.686, 0.216)
DARK = (0.07, 0.03, 0.09)

REPL = {
    "\x14": " — ",
    "\x97": "—",
    "\x96": "–",
    "\x92": " → ",
    "\x91": "'",
    "\x93": '"',
    "\x94": '"',
    "\xb7": "·",
    "\x85": "...",
    "\xa0": " ",
}

PAGES = [
    ("drawings/ejl-lighthouse-logo.png", "EJL Lighthouse logo", "image"),
    ("drawings/01-indoor-floor-plan.svg", "A-01 Indoor level floor plan", "svg"),
    ("drawings/02-rooftop-floor-plan.svg", "A-02 Rooftop floor plan", "svg"),
    ("drawings/03-robot-routing.svg", "A-03 Robot routing", "svg"),
    ("drawings/04-section-elevation.svg", "A-04 Building section / elevation", "svg"),
    ("drawings/05-vip-room-plan.svg", "A-04 One VIP unit - lounge / office / bedroom", "svg"),
    ("drawings/06-emergency-room-plan.svg", "A-05 Emergency / seizure room", "svg"),
    ("drawings/09-staff-rest-changing-plan.svg", "A-06 Staff rest & changing (closets)", "svg"),
    ("drawings/07-payment-system.svg", "P-01 Electronic payment (no tip)", "svg"),
    ("drawings/08-robot-branding.svg", "B-01 Robot branding", "svg"),
    ("images/00-ejl-lighthouse-logo.png", "Brand - EJL Lighthouse", "image"),
    ("images/10-classic-fountain-display.png", "Classic fountain display", "image"),
    ("images/11-classic-fountain-detail.png", "Classic fountain detail", "image"),
    ("images/12-classic-fireplace.png", "Classic fireplace", "image"),
    ("images/13-classic-fireplace-detail.png", "Classic fireplace detail", "image"),
    ("images/14-classic-pole-dance.png", "Classic pole dance stage", "image"),
    ("images/15-vip-suite-full.png", "VIP suite - full concept", "image"),
    ("images/16-vip-suite-earlier.png", "VIP suite - earlier concept", "image"),
    ("images/17-vip-bedroom.png", "VIP bedroom", "image"),
    ("images/18-vip-office.png", "VIP private office", "image"),
    ("images/19-vip-office-bedroom-suite.png", "One VIP cutaway - office + bedroom", "image"),
    ("images/20-rooftop-concept.png", "Rooftop concept", "image"),
    ("images/21-indoor-robot-concept.png", "Indoor robot concept", "image"),
    ("images/22-building-section-concept.png", "Building section concept", "image"),
    ("images/23-emergency-room.png", "Emergency room concept", "image"),
    ("images/24-staff-rest-changing.png", "Staff rest & changing with closets", "image"),
]


def sanitize_svg_bytes(raw: bytes) -> bytes:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
    for a, b in REPL.items():
        text = text.replace(a, b)
    text = "".join(ch if (ch >= " " or ch in "\n\t\r") else " " for ch in text)
    text = re.sub(r'\smarker-end="url\([^"]+\)"', "", text)
    text = re.sub(r'\smarker-start="url\([^"]+\)"', "", text)
    if not text.lstrip().startswith("<?xml"):
        text = '<?xml version="1.0" encoding="UTF-8"?>\n' + text
    return text.encode("utf-8")


def load_image(path: Path, kind: str) -> Image.Image:
    if kind == "svg":
        png_bytes = cairosvg.svg2png(bytestring=sanitize_svg_bytes(path.read_bytes()), dpi=150)
        return Image.open(BytesIO(png_bytes)).convert("RGB")
    img = Image.open(path)
    if img.mode in ("RGBA", "P"):
        bg = Image.new("RGB", img.size, (18, 8, 22))
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
        return bg
    return img.convert("RGB")


def main() -> None:
    pages = []
    for rel, title, kind in PAGES:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"missing: {rel}")
        pages.append((path, title, kind))

    OUT.parent.mkdir(exist_ok=True)
    page = landscape(A4)
    w, h = page
    c = canvas.Canvas(str(OUT), pagesize=page)

    c.setFillColorRGB(*DARK)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColorRGB(*PINK)
    c.rect(0, h - 18 * mm, w, 8 * mm, fill=1, stroke=0)
    c.setFillColorRGB(*GOLD)
    c.rect(0, 0, w, 6 * mm, fill=1, stroke=0)
    c.setFillColorRGB(*PINK)
    c.setFont("Times-Bold", 36)
    c.drawCentredString(w / 2, h / 2 + 40, "EJL LIGHTHOUSE")
    c.setFillColorRGB(*GOLD)
    c.setFont("Times-Bold", 20)
    c.drawCentredString(w / 2, h / 2 + 10, "Dubai - Architecture Drawings & Images")
    c.setFillColorRGB(1, 0.71, 0.85)
    c.setFont("Helvetica", 12)
    c.drawCentredString(
        w / 2,
        h / 2 - 25,
        "One VIP (lounge / office / bedroom) · Emergency room · Staff rest & changing",
    )
    c.setFont("Helvetica", 10)
    c.drawCentredString(w / 2, h / 2 - 45, f"{len(pages)} image sheets + cover + contents")
    c.setFillColorRGB(*GOLD)
    c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, 20 * mm, "All drawings and images in one PDF")
    c.showPage()

    c.setFillColorRGB(*DARK)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColorRGB(*PINK)
    c.setFont("Times-Bold", 22)
    c.drawString(25 * mm, h - 25 * mm, "Contents")
    y = h - 40 * mm
    col2 = False
    for i, (path, title, kind) in enumerate(pages, 1):
        c.setFillColorRGB(*GOLD)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(25 * mm if not col2 else w / 2, y, f"{i:02d}")
        c.setFillColorRGB(1, 0.9, 0.95)
        c.setFont("Helvetica", 10)
        c.drawString(35 * mm if not col2 else w / 2 + 10 * mm, y, title[:52])
        y -= 7 * mm
        if y < 20 * mm and not col2:
            col2 = True
            y = h - 40 * mm
    c.showPage()

    margin, header, footer = 15 * mm, 14 * mm, 10 * mm
    for idx, (path, title, kind) in enumerate(pages, 1):
        c.setFillColorRGB(*DARK)
        c.rect(0, 0, w, h, fill=1, stroke=0)
        c.setFillColorRGB(0.1, 0.04, 0.12)
        c.rect(0, h - header, w, header, fill=1, stroke=0)
        c.setFillColorRGB(*PINK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin, h - header + 4 * mm, title)
        c.setFillColorRGB(*GOLD)
        c.setFont("Helvetica", 9)
        c.drawRightString(w - margin, h - header + 4 * mm, f"{idx} / {len(pages)}")
        c.setFillColorRGB(0.1, 0.04, 0.12)
        c.rect(0, 0, w, footer, fill=1, stroke=0)
        c.setFillColorRGB(*GOLD)
        c.setFont("Helvetica", 8)
        c.drawString(margin, 3.5 * mm, "EJL Lighthouse - Dubai")
        c.drawRightString(w - margin, 3.5 * mm, path.name)

        img = load_image(path, kind)
        avail_w = w - 2 * margin
        avail_h = h - header - footer - 8 * mm
        iw, ih = img.size
        scale = min(avail_w / iw, avail_h / ih)
        dw, dh = iw * scale, ih * scale
        x = (w - dw) / 2
        y = footer + (avail_h - dh) / 2 + 2 * mm
        c.setStrokeColorRGB(*GOLD)
        c.setLineWidth(1)
        c.rect(x - 2, y - 2, dw + 4, dh + 4, fill=0, stroke=1)
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=85, optimize=True)
        buf.seek(0)
        c.drawImage(ImageReader(buf), x, y, width=dw, height=dh, preserveAspectRatio=True, mask="auto")
        c.showPage()
        print("OK", idx, path.name)

    c.save()
    shutil.copy2(OUT, OUT_COPY)
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
