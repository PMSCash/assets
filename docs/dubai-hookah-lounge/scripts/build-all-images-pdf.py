#!/usr/bin/env python3
"""Build A4 all-images PDF and A1 print boards for EJL Lighthouse."""
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
OUT_A4 = ROOT / "download" / "EJL-Lighthouse-all-images.pdf"
OUT_A4_COPY = ROOT / "EJL-Lighthouse-all-images.pdf"
OUT_A1 = ROOT / "download" / "EJL-Lighthouse-A1-boards.pdf"

PINK = (1.0, 0.176, 0.584)
GOLD = (0.831, 0.686, 0.216)
DARK = (0.07, 0.03, 0.09)

# A1 landscape mm
A1_LANDSCAPE = (841 * mm, 594 * mm)

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
    ("drawings/02-rooftop-floor-plan.svg", "A-02 Rooftop floor plan (+ VIP-2)", "svg"),
    ("drawings/03-robot-routing.svg", "A-03 Robot routing", "svg"),
    ("drawings/04-section-elevation.svg", "A-04 Building section / elevation", "svg"),
    ("drawings/05-vip-room-plan.svg", "A-04 VIP-1 - lounge / office / bedroom", "svg"),
    ("drawings/06-emergency-room-plan.svg", "A-05 Emergency / seizure room", "svg"),
    ("drawings/09-staff-rest-changing-plan.svg", "A-06 Staff rest & changing (closets)", "svg"),
    ("drawings/10-rooftop-vip-plan.svg", "A-07 Rooftop VIP-2", "svg"),
    ("drawings/11-kitchen-boh-plan.svg", "A-08 Kitchen / BOH", "svg"),
    ("drawings/12-mep-systems.svg", "M-01 MEP systems", "svg"),
    ("drawings/13-ffe-schedule.svg", "F-01 FF&E schedule", "svg"),
    ("drawings/14-guest-journey.svg", "G-01 Guest journey", "svg"),
    ("drawings/07-payment-system.svg", "P-01 Electronic payment", "svg"),
    ("drawings/08-robot-branding.svg", "B-01 Robot branding", "svg"),
    ("images/10-classic-fountain-display.png", "Classic fountain display", "image"),
    ("images/11-classic-fountain-detail.png", "Classic fountain detail", "image"),
    ("images/12-classic-fireplace.png", "Classic fireplace", "image"),
    ("images/13-classic-fireplace-detail.png", "Classic fireplace detail", "image"),
    ("images/14-classic-pole-dance.png", "Classic pole dance stage", "image"),
    ("images/15-vip-suite-full.png", "VIP-1 suite full concept", "image"),
    ("images/16-vip-suite-earlier.png", "VIP suite earlier concept", "image"),
    ("images/17-vip-bedroom.png", "VIP-1 bedroom", "image"),
    ("images/18-vip-office.png", "VIP-1 private office", "image"),
    ("images/19-vip-office-bedroom-suite.png", "VIP-1 cutaway office + bedroom", "image"),
    ("images/20-rooftop-concept.png", "Rooftop concept", "image"),
    ("images/21-indoor-robot-concept.png", "Indoor robot concept", "image"),
    ("images/22-building-section-concept.png", "Building section concept", "image"),
    ("images/23-emergency-room.png", "Emergency room concept", "image"),
    ("images/24-staff-rest-changing.png", "Staff rest & changing", "image"),
    ("images/25-rooftop-vip.png", "Rooftop VIP-2 concept", "image"),
    ("images/26-kitchen-boh.png", "Kitchen BOH concept", "image"),
    ("images/27-mep-systems.png", "MEP systems concept", "image"),
    ("images/28-ffe-mood.png", "FF&E mood board", "image"),
    ("images/29-guest-journey.png", "Guest journey concept", "image"),
]

A1_BOARDS = [
    ("drawings/01-indoor-floor-plan.svg", "A1 BOARD · A-01 Indoor floor plan", "svg"),
    ("drawings/05-vip-room-plan.svg", "A1 BOARD · A-04 VIP-1 office + bedroom", "svg"),
    ("drawings/10-rooftop-vip-plan.svg", "A1 BOARD · A-07 Rooftop VIP-2", "svg"),
    ("drawings/06-emergency-room-plan.svg", "A1 BOARD · A-05 Emergency room", "svg"),
    ("drawings/09-staff-rest-changing-plan.svg", "A1 BOARD · A-06 Staff rest & changing", "svg"),
    ("drawings/11-kitchen-boh-plan.svg", "A1 BOARD · A-08 Kitchen / BOH", "svg"),
    ("drawings/12-mep-systems.svg", "A1 BOARD · M-01 MEP systems", "svg"),
    ("drawings/14-guest-journey.svg", "A1 BOARD · G-01 Guest journey", "svg"),
    ("drawings/13-ffe-schedule.svg", "A1 BOARD · F-01 FF&E schedule", "svg"),
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


def load_image(path: Path, kind: str, dpi: int = 150) -> Image.Image:
    if kind == "svg":
        png_bytes = cairosvg.svg2png(bytestring=sanitize_svg_bytes(path.read_bytes()), dpi=dpi)
        return Image.open(BytesIO(png_bytes)).convert("RGB")
    img = Image.open(path)
    if img.mode in ("RGBA", "P"):
        bg = Image.new("RGB", img.size, (18, 8, 22))
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
        return bg
    return img.convert("RGB")


def draw_pdf(out: Path, pages: list, page_size, dpi: int = 150, title_main: str = "EJL LIGHTHOUSE") -> None:
    out.parent.mkdir(exist_ok=True)
    w, h = page_size
    c = canvas.Canvas(str(out), pagesize=page_size)

    c.setFillColorRGB(*DARK)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColorRGB(*PINK)
    c.rect(0, h - 18 * mm, w, 8 * mm, fill=1, stroke=0)
    c.setFillColorRGB(*GOLD)
    c.rect(0, 0, w, 6 * mm, fill=1, stroke=0)
    c.setFillColorRGB(*PINK)
    c.setFont("Times-Bold", 36 if w < 700 * mm else 48)
    c.drawCentredString(w / 2, h / 2 + 40, title_main)
    c.setFillColorRGB(*GOLD)
    c.setFont("Times-Bold", 18 if w < 700 * mm else 26)
    c.drawCentredString(w / 2, h / 2 + 5, "Dubai - Architecture Drawings & Images")
    c.setFillColorRGB(1, 0.71, 0.85)
    c.setFont("Helvetica", 11 if w < 700 * mm else 16)
    c.drawCentredString(w / 2, h / 2 - 30, f"{len(pages)} sheets · VIP-1/2 · Emergency · Staff · Kitchen · MEP · Journey")
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
        c.setFont("Helvetica-Bold", 9 if w < 700 * mm else 12)
        c.drawString(25 * mm if not col2 else w / 2, y, f"{i:02d}")
        c.setFillColorRGB(1, 0.9, 0.95)
        c.setFont("Helvetica", 9 if w < 700 * mm else 12)
        c.drawString(34 * mm if not col2 else w / 2 + 12 * mm, y, title[:56])
        y -= 6.2 * mm if w < 700 * mm else 8 * mm
        if y < 20 * mm and not col2:
            col2 = True
            y = h - 40 * mm
    c.showPage()

    margin, header, footer = 15 * mm, 14 * mm, 10 * mm
    if w >= 700 * mm:
        margin, header, footer = 25 * mm, 20 * mm, 14 * mm

    for idx, (path, title, kind) in enumerate(pages, 1):
        c.setFillColorRGB(*DARK)
        c.rect(0, 0, w, h, fill=1, stroke=0)
        c.setFillColorRGB(0.1, 0.04, 0.12)
        c.rect(0, h - header, w, header, fill=1, stroke=0)
        c.setFillColorRGB(*PINK)
        c.setFont("Helvetica-Bold", 11 if w < 700 * mm else 16)
        c.drawString(margin, h - header + 4 * mm, title)
        c.setFillColorRGB(*GOLD)
        c.setFont("Helvetica", 9 if w < 700 * mm else 12)
        c.drawRightString(w - margin, h - header + 4 * mm, f"{idx} / {len(pages)}")
        c.setFillColorRGB(0.1, 0.04, 0.12)
        c.rect(0, 0, w, footer, fill=1, stroke=0)
        c.setFillColorRGB(*GOLD)
        c.setFont("Helvetica", 8 if w < 700 * mm else 11)
        c.drawString(margin, 3.5 * mm, "EJL Lighthouse - Dubai")
        c.drawRightString(w - margin, 3.5 * mm, path.name)

        img = load_image(path, kind, dpi=dpi)
        avail_w = w - 2 * margin
        avail_h = h - header - footer - 8 * mm
        iw, ih = img.size
        scale = min(avail_w / iw, avail_h / ih)
        dw, dh = iw * scale, ih * scale
        x = (w - dw) / 2
        y = footer + (avail_h - dh) / 2 + 2 * mm
        c.setStrokeColorRGB(*GOLD)
        c.setLineWidth(1.5)
        c.rect(x - 3, y - 3, dw + 6, dh + 6, fill=0, stroke=1)
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=82, optimize=True)
        buf.seek(0)
        c.drawImage(ImageReader(buf), x, y, width=dw, height=dh, preserveAspectRatio=True, mask="auto")
        c.showPage()
        print("OK", out.name, idx, path.name)

    c.save()
    print(f"Wrote {out} ({out.stat().st_size / 1024 / 1024:.1f} MB)")


def main() -> None:
    pages = []
    for rel, title, kind in PAGES:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"missing: {rel}")
        pages.append((path, title, kind))

    a1_pages = []
    for rel, title, kind in A1_BOARDS:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"missing A1: {rel}")
        a1_pages.append((path, title, kind))

    draw_pdf(OUT_A4, pages, landscape(A4), dpi=140, title_main="EJL LIGHTHOUSE")
    shutil.copy2(OUT_A4, OUT_A4_COPY)
    draw_pdf(OUT_A1, a1_pages, A1_LANDSCAPE, dpi=160, title_main="EJL LIGHTHOUSE · A1")


if __name__ == "__main__":
    main()
