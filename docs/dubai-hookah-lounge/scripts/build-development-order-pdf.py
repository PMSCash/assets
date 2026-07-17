#!/usr/bin/env python3
"""
Scan all EJL Lighthouse folders, extract unique images, and build one PDF
ordered by development / execution sequence — each sheet has a definition.
"""
from __future__ import annotations

import hashlib
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
OUT = ROOT / "download" / "EJL-Lighthouse-development-order.pdf"
OUT_COPY = ROOT / "EJL-Lighthouse-development-order.pdf"

PINK = (1.0, 0.176, 0.584)
GOLD = (0.831, 0.686, 0.216)
DARK = (0.07, 0.03, 0.09)
INK = (1.0, 0.92, 0.95)
MUTED = (1.0, 0.71, 0.85)

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

# Development / execution order — how the project should be built.
# Prefer images/ paths when both drawings/ and images/ hold the same visual.
SEQUENCE: list[dict] = [
    # PHASE 0 — Brand & brief
    {
        "phase": "0 · BRAND & BRIEF",
        "phase_note": "Lock identity before design freeze.",
        "path": "images/00-ejl-lighthouse-logo.png",
        "code": "B-00",
        "title": "EJL Lighthouse brand mark",
        "definition": "Official pink/gold house logo. Apply to robots, VIP plaques, tray liners, staff closet tags, and app. Establishes brand before any FF&E orders.",
    },
    # PHASE 1 — Vision atmospheres (design intent)
    {
        "phase": "1 · DESIGN INTENT / SIGNATURE FEATURES",
        "phase_note": "Freeze the look of signature guest features.",
        "path": "images/10-classic-fountain-display.png",
        "code": "C-01",
        "title": "Classic indoor fountain — display",
        "definition": "Primary fountain atmosphere for dining and VIP-1. Pink LED wash, waterproofing + drain, robot keep-out ring ~0.8 m.",
    },
    {
        "phase": "1 · DESIGN INTENT / SIGNATURE FEATURES",
        "path": "images/11-classic-fountain-detail.png",
        "code": "C-02",
        "title": "Classic indoor fountain — detail",
        "definition": "Close-up finish reference for fountain basin, water jet, and gold/pink lighting. Use for FF&E vendor briefing.",
    },
    {
        "phase": "1 · DESIGN INTENT / SIGNATURE FEATURES",
        "path": "images/12-classic-fireplace.png",
        "code": "C-03",
        "title": "Classic gas fireplace",
        "definition": "VIP fireplace with gold surround. Civil Defense–compliant sealed/gas unit with guard. Required in VIP-1 and outdoor form in VIP-2.",
    },
    {
        "phase": "1 · DESIGN INTENT / SIGNATURE FEATURES",
        "path": "images/13-classic-fireplace-detail.png",
        "code": "C-04",
        "title": "Classic fireplace — detail",
        "definition": "Material and flame presentation detail for fireplace procurement and installation drawings.",
    },
    {
        "phase": "1 · DESIGN INTENT / SIGNATURE FEATURES",
        "path": "images/14-classic-pole-dance.png",
        "code": "C-05",
        "title": "Classic pole dance stage",
        "definition": "Chrome pole on circular stage with soft floor and pink uplight. VIP-1 only. Clear height 2.4 m minimum.",
    },
    {
        "phase": "1 · DESIGN INTENT / SIGNATURE FEATURES",
        "path": "images/20-rooftop-concept.png",
        "code": "C-06",
        "title": "Rooftop lounge atmosphere",
        "definition": "Overall rooftop vision: pergola, reflective linear ceiling lights, city skyline. Sets outdoor FF&E and lighting direction.",
    },
    {
        "phase": "1 · DESIGN INTENT / SIGNATURE FEATURES",
        "path": "images/21-indoor-robot-concept.png",
        "code": "C-07",
        "title": "Indoor robot + fountain atmosphere",
        "definition": "Shows EJL-branded delivery robots operating beside the indoor fountain. Confirms robot aisle and keep-out zones early.",
    },
    # PHASE 2 — Guest journey (ops story before walls)
    {
        "phase": "2 · GUEST JOURNEY / OPS STORY",
        "phase_note": "Define how guests and staff move before freezing walls.",
        "path": "drawings/14-guest-journey.svg",
        "code": "G-01",
        "title": "Guest journey map — entry → VIP → pay",
        "definition": "Operational sequence: Arrive → Escort → Unlock → Experience → Service → E-pay → Donation → Depart. Includes VIP-2 and medical panic alternates.",
    },
    {
        "phase": "2 · GUEST JOURNEY / OPS STORY",
        "path": "images/29-guest-journey.png",
        "code": "G-01a",
        "title": "Guest journey concept render",
        "definition": "Visual storyboard of host arrival, fountain passage, VIP e-door, and electronic payment. Aligns brand experience with G-01.",
    },
    {
        "phase": "2 · GUEST JOURNEY / OPS STORY",
        "path": "drawings/07-payment-system.svg",
        "code": "P-01",
        "title": "Payment system — electronic only",
        "definition": "No cash, no tipping. NFC/QR/wallets only. Optional donation after receipt to house fund/charity — never to staff.",
    },
    {
        "phase": "2 · GUEST JOURNEY / OPS STORY",
        "path": "drawings/03-robot-routing.svg",
        "code": "R-01",
        "title": "Robot routing & order flow",
        "definition": "Order lifecycle: QR → POS → KDS → load bay → robot → table. Hard virtual walls at VIP, coal, emergency, staff rooms.",
    },
    {
        "phase": "2 · GUEST JOURNEY / OPS STORY",
        "path": "drawings/08-robot-branding.svg",
        "code": "B-01",
        "title": "Robot fleet branding",
        "definition": "EJL pink/gold livery standard for R1–R4: front circular mark, side wordmark, tray liners. Apply before fleet delivery.",
    },
    # PHASE 3 — Shell & MEP (build structure first)
    {
        "phase": "3 · BUILDING SHELL & MEP",
        "phase_note": "Structure, exhaust, HVAC, and fire before fit-out.",
        "path": "drawings/04-section-elevation.svg",
        "code": "A-03",
        "title": "Building section / elevation",
        "definition": "Cut through indoor + rooftop levels showing vertical relationships for stairs/lift, exhaust, and fountain.",
    },
    {
        "phase": "3 · BUILDING SHELL & MEP",
        "path": "images/22-building-section-concept.png",
        "code": "A-03a",
        "title": "Building section concept render",
        "definition": "Atmospheric section concept supporting A-03 for landlord / consultant briefings.",
    },
    {
        "phase": "3 · BUILDING SHELL & MEP",
        "path": "drawings/12-mep-systems.svg",
        "code": "M-01",
        "title": "MEP systems — coal · HVAC · fire",
        "definition": "Dedicated coal stacks, separate kitchen hood, pressure cascade, sprinklers, fail-safe VIP e-doors. Civil Defense pre-consult required. Not issued CD drawings.",
    },
    {
        "phase": "3 · BUILDING SHELL & MEP",
        "path": "images/27-mep-systems.png",
        "code": "M-01a",
        "title": "MEP systems concept render",
        "definition": "Visual of roof plant, coal exhaust, and building systems intent for MEP consultant kickoff.",
    },
    # PHASE 4 — Floor plans (spatial freeze)
    {
        "phase": "4 · SPATIAL PLANS (FREEZE FOOTPRINT)",
        "phase_note": "Lock room adjacency and clear widths.",
        "path": "drawings/01-indoor-floor-plan.svg",
        "code": "A-01",
        "title": "Indoor level floor plan",
        "definition": "Host, dining, fountain, massage, e-shisha, VIP-1, kitchen/robot bay, coal room, emergency, staff rest/change, guest WC, stairs/lift.",
    },
    {
        "phase": "4 · SPATIAL PLANS (FREEZE FOOTPRINT)",
        "path": "drawings/02-rooftop-floor-plan.svg",
        "code": "A-02",
        "title": "Rooftop floor plan (+ VIP-2)",
        "definition": "28-seat rooftop lounge under pergola; VIP-2 e-locked terrace overlays/replaces 8 seats when booked; exhaust stacks and bar handoff.",
    },
    # PHASE 5 — Core BOH build
    {
        "phase": "5 · KITCHEN / BOH BUILD",
        "phase_note": "Fit kitchen and robot bay before FOH finishes.",
        "path": "drawings/11-kitchen-boh-plan.svg",
        "code": "A-08",
        "title": "Kitchen / BOH plan",
        "definition": "Prep, cook line, dish, cold/dry stores, robot loading bay, dumbwaiter to rooftop. Staff only; robots only in bay.",
    },
    {
        "phase": "5 · KITCHEN / BOH BUILD",
        "path": "images/26-kitchen-boh.png",
        "code": "A-08a",
        "title": "Kitchen / BOH concept render",
        "definition": "Finish reference for stainless cook line, dish area, and tray pass to robot bay.",
    },
    # PHASE 6 — Safety & staff rooms
    {
        "phase": "6 · SAFETY & STAFF ROOMS",
        "phase_note": "Life-safety and workforce rooms before guest opening.",
        "path": "drawings/06-emergency-room-plan.svg",
        "code": "A-05",
        "title": "Emergency / seizure room plan",
        "definition": "First-response room: treatment bed, O2, suction, AED, seizure kit, stretcher, EMS route. Adjacent to staff rest. Robots forbidden.",
    },
    {
        "phase": "6 · SAFETY & STAFF ROOMS",
        "path": "images/23-emergency-room.png",
        "code": "A-05a",
        "title": "Emergency room concept render",
        "definition": "Clinical fit-out look for A-05 equipment layout and privacy curtain.",
    },
    {
        "phase": "6 · SAFETY & STAFF ROOMS",
        "path": "drawings/09-staff-rest-changing-plan.svg",
        "code": "A-06",
        "title": "Staff rest & changing (closets)",
        "definition": "Workers-only: rest sofas, W/M changing booths, lockable closets C01–C12, uniform closet, shoe rack, staff WC, phone cubbies.",
    },
    {
        "phase": "6 · SAFETY & STAFF ROOMS",
        "path": "images/24-staff-rest-changing.png",
        "code": "A-06a",
        "title": "Staff rest & changing concept render",
        "definition": "Visual of lockers/closets and changing zone finishes for BOH FF&E order.",
    },
    # PHASE 7 — VIP-1 principal suite
    {
        "phase": "7 · VIP-1 PRINCIPAL SUITE (INDOOR)",
        "phase_note": "Fit the flagship e-locked unit last among major rooms.",
        "path": "drawings/05-vip-room-plan.svg",
        "code": "A-04",
        "title": "VIP-1 plan — lounge · office · bedroom",
        "definition": "One principal VIP (~90 m²): entertainment lounge with fountain/fireplace/pole/TVs, private office, bedroom + ensuite, hostess, service pass, e-lock.",
    },
    {
        "phase": "7 · VIP-1 PRINCIPAL SUITE (INDOOR)",
        "path": "images/15-vip-suite-full.png",
        "code": "A-04a",
        "title": "VIP-1 suite — full concept",
        "definition": "Complete EJL VIP entertainment look: fountain, fireplace, pole, pink/gold finishes.",
    },
    {
        "phase": "7 · VIP-1 PRINCIPAL SUITE (INDOOR)",
        "path": "images/16-vip-suite-earlier.png",
        "code": "A-04b",
        "title": "VIP suite — earlier concept",
        "definition": "Earlier VIP direction retained for design history / option comparison.",
    },
    {
        "phase": "7 · VIP-1 PRINCIPAL SUITE (INDOOR)",
        "path": "images/18-vip-office.png",
        "code": "A-04c",
        "title": "VIP-1 private office",
        "definition": "Sound-sealed office for principal: exec desk, monitor wall, sofa, in-room safe. Robots never enter.",
    },
    {
        "phase": "7 · VIP-1 PRINCIPAL SUITE (INDOOR)",
        "path": "images/17-vip-bedroom.png",
        "code": "A-04d",
        "title": "VIP-1 bedroom",
        "definition": "King bedroom with blackout, wardrobe, 55\" TV, ensuite. Panic button to emergency room.",
    },
    {
        "phase": "7 · VIP-1 PRINCIPAL SUITE (INDOOR)",
        "path": "images/19-vip-office-bedroom-suite.png",
        "code": "A-04e",
        "title": "VIP-1 cutaway — lounge + office + bedroom",
        "definition": "Shows the three-room relationship behind one e-locked vestibule for contractor coordination.",
    },
    # PHASE 8 — VIP-2 rooftop add-on
    {
        "phase": "8 · VIP-2 ROOFTOP ADD-ON",
        "phase_note": "Build after rooftop shell and VIP-1 lessons.",
        "path": "drawings/10-rooftop-vip-plan.svg",
        "code": "A-07",
        "title": "Rooftop VIP-2 plan",
        "definition": "~55 m² e-locked terrace: pergola, outdoor fireplace, weather TV, 8 seats, hostess, R4 pass. No office/bedroom. Replaces 8 rooftop seats when booked.",
    },
    {
        "phase": "8 · VIP-2 ROOFTOP ADD-ON",
        "path": "images/25-rooftop-vip.png",
        "code": "A-07a",
        "title": "Rooftop VIP-2 concept render",
        "definition": "Night terrace atmosphere for VIP-2 FF&E and lighting.",
    },
    # PHASE 9 — Procurement / opening
    {
        "phase": "9 · PROCUREMENT & OPENING",
        "phase_note": "Order FF&E and train staff before soft open.",
        "path": "drawings/13-ffe-schedule.svg",
        "code": "F-01",
        "title": "FF&E schedule — quantities",
        "definition": "Indicative counts: seats, TVs, robots, closets C01–C12, kitchen modules, clinical kit. Pink/gold finish standard. Not a purchase order.",
    },
    {
        "phase": "9 · PROCUREMENT & OPENING",
        "path": "images/28-ffe-mood.png",
        "code": "F-01a",
        "title": "FF&E mood board",
        "definition": "Visual procurement board for banquettes, VIP bed/desk, massage seats, fountain, fireplace, pole, lockers, robot tray.",
    },
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


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_image(path: Path) -> Image.Image:
    if path.suffix.lower() == ".svg":
        png_bytes = cairosvg.svg2png(bytestring=sanitize_svg_bytes(path.read_bytes()), dpi=140)
        return Image.open(BytesIO(png_bytes)).convert("RGB")
    img = Image.open(path)
    if img.mode in ("RGBA", "P"):
        bg = Image.new("RGB", img.size, (18, 8, 22))
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
        return bg
    return img.convert("RGB")


def scan_all_assets() -> list[Path]:
    assets: list[Path] = []
    for folder in (ROOT / "images", ROOT / "drawings"):
        if not folder.exists():
            continue
        for p in sorted(folder.iterdir()):
            if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".webp"}:
                assets.append(p)
    return assets


def wrap_text(c: canvas.Canvas, text: str, x: float, y: float, max_width: float, font: str, size: int, leading: float, color):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    words = text.split()
    line = ""
    for w in words:
        trial = (line + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_width:
            line = trial
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def build() -> None:
    # Validate sequence paths and collect hashes of included files
    pages = []
    included_hashes: set[str] = set()
    for item in SEQUENCE:
        path = ROOT / item["path"]
        if not path.exists():
            raise SystemExit(f"missing sequenced asset: {item['path']}")
        pages.append({**item, "abs": path})
        included_hashes.add(file_hash(path))

    # Report any scanned assets not in the development sequence (duplicates OK if hash matches)
    leftovers = []
    for p in scan_all_assets():
        h = file_hash(p)
        if h in included_hashes:
            continue
        # skip logo svg if logo png included, and known drawings-only duplicates of images/
        leftovers.append(p.relative_to(ROOT).as_posix())

    OUT.parent.mkdir(exist_ok=True)
    page = landscape(A4)
    w, h = page
    c = canvas.Canvas(str(OUT), pagesize=page)

    # ===== COVER =====
    c.setFillColorRGB(*DARK)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColorRGB(*PINK)
    c.rect(0, h - 18 * mm, w, 8 * mm, fill=1, stroke=0)
    c.setFillColorRGB(*GOLD)
    c.rect(0, 0, w, 6 * mm, fill=1, stroke=0)
    c.setFillColorRGB(*PINK)
    c.setFont("Times-Bold", 32)
    c.drawCentredString(w / 2, h / 2 + 50, "EJL LIGHTHOUSE")
    c.setFillColorRGB(*GOLD)
    c.setFont("Times-Bold", 18)
    c.drawCentredString(w / 2, h / 2 + 18, "Development-Order Image Book")
    c.setFillColorRGB(*MUTED)
    c.setFont("Helvetica", 11)
    c.drawCentredString(w / 2, h / 2 - 15, "All folders scanned · unique images extracted · definitions · build sequence")
    c.setFont("Helvetica", 10)
    c.drawCentredString(w / 2, h / 2 - 35, f"{len(pages)} sheets in 10 execution phases · Dubai concept package")
    c.setFillColorRGB(*GOLD)
    c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, 22 * mm, "Scan sources: images/ · drawings/ · docs/dubai-hookah-lounge/")
    c.showPage()

    # ===== HOW TO EXECUTE =====
    c.setFillColorRGB(*DARK)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColorRGB(*PINK)
    c.setFont("Times-Bold", 22)
    c.drawString(25 * mm, h - 25 * mm, "Execution order (read top → bottom)")
    steps = [
        "0 Brand & brief — lock EJL pink/gold identity",
        "1 Design intent — freeze fountain, fireplace, pole, rooftop atmosphere",
        "2 Guest journey / ops — journey, pay rules, robot routing & branding",
        "3 Building shell & MEP — section + coal/HVAC/fire schematic (CD pre-consult)",
        "4 Spatial plans — freeze indoor + rooftop footprints and clear widths",
        "5 Kitchen / BOH — prep, cook, dish, stores, robot bay, dumbwaiter",
        "6 Safety & staff — emergency room + staff rest/changing with closets",
        "7 VIP-1 — indoor principal suite (lounge + office + bedroom)",
        "8 VIP-2 — rooftop terrace add-on after shell and VIP-1 lessons",
        "9 Procurement & opening — FF&E quantities, vendor orders, training, soft open",
    ]
    y = h - 42 * mm
    for s in steps:
        c.setFillColorRGB(*GOLD)
        c.setFont("Helvetica-Bold", 12)
        num = s.split(" ", 1)[0]
        rest = s.split(" ", 1)[1] if " " in s else s
        c.drawString(28 * mm, y, num)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica", 11)
        c.drawString(40 * mm, y, rest)
        y -= 10 * mm
    c.setFillColorRGB(*MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(28 * mm, 20 * mm, "Each following page = one asset + definition aligned to this sequence.")
    c.showPage()

    # ===== CONTENTS =====
    c.setFillColorRGB(*DARK)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColorRGB(*PINK)
    c.setFont("Times-Bold", 20)
    c.drawString(20 * mm, h - 22 * mm, "Contents — development alignment")
    y = h - 35 * mm
    col2 = False
    for i, item in enumerate(pages, 1):
        c.setFillColorRGB(*GOLD)
        c.setFont("Helvetica-Bold", 8)
        x0 = 20 * mm if not col2 else w / 2 + 2 * mm
        c.drawString(x0, y, f"{i:02d} {item['code']}")
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica", 8)
        c.drawString(x0 + 22 * mm, y, item["title"][:42])
        y -= 5.4 * mm
        if y < 18 * mm and not col2:
            col2 = True
            y = h - 35 * mm
    c.showPage()

    # ===== ASSET PAGES =====
    margin = 12 * mm
    def_w = 72 * mm
    img_left = margin
    img_right = w - margin - def_w - 6 * mm
    header = 12 * mm
    footer = 9 * mm
    current_phase = None

    for idx, item in enumerate(pages, 1):
        # phase divider when phase changes
        if item["phase"] != current_phase:
            current_phase = item["phase"]
            c.setFillColorRGB(*DARK)
            c.rect(0, 0, w, h, fill=1, stroke=0)
            c.setFillColorRGB(*PINK)
            c.setFont("Times-Bold", 26)
            c.drawCentredString(w / 2, h / 2 + 20, current_phase)
            note = item.get("phase_note") or ""
            # find first note for this phase from SEQUENCE
            for s in SEQUENCE:
                if s["phase"] == current_phase and s.get("phase_note"):
                    note = s["phase_note"]
                    break
            c.setFillColorRGB(*GOLD)
            c.setFont("Helvetica", 12)
            c.drawCentredString(w / 2, h / 2 - 10, note)
            c.setFillColorRGB(*MUTED)
            c.setFont("Helvetica", 10)
            c.drawCentredString(w / 2, h / 2 - 30, "Development phase divider")
            c.showPage()

        c.setFillColorRGB(*DARK)
        c.rect(0, 0, w, h, fill=1, stroke=0)
        # header
        c.setFillColorRGB(0.1, 0.04, 0.12)
        c.rect(0, h - header, w, header, fill=1, stroke=0)
        c.setFillColorRGB(*PINK)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin, h - header + 3.5 * mm, f"{item['code']}  ·  {item['title']}")
        c.setFillColorRGB(*GOLD)
        c.setFont("Helvetica", 8)
        c.drawRightString(w - margin, h - header + 3.5 * mm, f"{idx} / {len(pages)}")

        # footer
        c.setFillColorRGB(0.1, 0.04, 0.12)
        c.rect(0, 0, w, footer, fill=1, stroke=0)
        c.setFillColorRGB(*GOLD)
        c.setFont("Helvetica", 7)
        c.drawString(margin, 3 * mm, item["phase"])
        c.drawRightString(w - margin, 3 * mm, item["path"])

        # definition panel (right)
        panel_x = w - margin - def_w
        panel_y = footer + 4 * mm
        panel_h = h - header - footer - 8 * mm
        c.setFillColorRGB(0.08, 0.03, 0.1)
        c.setStrokeColorRGB(*GOLD)
        c.setLineWidth(1)
        c.roundRect(panel_x, panel_y, def_w, panel_h, 4, fill=1, stroke=1)

        ty = panel_y + panel_h - 10 * mm
        c.setFillColorRGB(*PINK)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(panel_x + 4 * mm, ty, "DEFINITION")
        ty -= 7 * mm
        c.setFillColorRGB(*GOLD)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(panel_x + 4 * mm, ty, f"Code: {item['code']}")
        ty -= 5 * mm
        c.setFillColorRGB(*MUTED)
        c.setFont("Helvetica", 7)
        c.drawString(panel_x + 4 * mm, ty, "Phase:")
        ty -= 4 * mm
        ty = wrap_text(c, item["phase"], panel_x + 4 * mm, ty, def_w - 8 * mm, "Helvetica", 7, 9, INK)
        ty -= 3 * mm
        c.setFillColorRGB(*MUTED)
        c.setFont("Helvetica", 7)
        c.drawString(panel_x + 4 * mm, ty, "Title:")
        ty -= 4 * mm
        ty = wrap_text(c, item["title"], panel_x + 4 * mm, ty, def_w - 8 * mm, "Helvetica-Bold", 8, 10, PINK)
        ty -= 3 * mm
        c.setFillColorRGB(*MUTED)
        c.setFont("Helvetica", 7)
        c.drawString(panel_x + 4 * mm, ty, "Definition:")
        ty -= 4 * mm
        ty = wrap_text(c, item["definition"], panel_x + 4 * mm, ty, def_w - 8 * mm, "Helvetica", 7.5, 10, INK)
        ty -= 4 * mm
        c.setFillColorRGB(*MUTED)
        c.setFont("Helvetica", 7)
        c.drawString(panel_x + 4 * mm, ty, "Source file:")
        ty -= 4 * mm
        wrap_text(c, item["path"], panel_x + 4 * mm, ty, def_w - 8 * mm, "Helvetica", 6.5, 8, GOLD)

        # image area
        try:
            img = load_image(item["abs"])
        except Exception as e:
            c.setFillColorRGB(1, 0.4, 0.4)
            c.setFont("Helvetica", 12)
            c.drawCentredString((img_left + img_right) / 2, h / 2, f"Failed: {item['path']} ({e})")
            c.showPage()
            continue

        avail_w = img_right - img_left
        avail_h = h - header - footer - 10 * mm
        iw, ih = img.size
        scale = min(avail_w / iw, avail_h / ih)
        dw, dh = iw * scale, ih * scale
        x = img_left + (avail_w - dw) / 2
        y = footer + 4 * mm + (avail_h - dh) / 2
        c.setStrokeColorRGB(*GOLD)
        c.setLineWidth(1)
        c.rect(x - 2, y - 2, dw + 4, dh + 4, fill=0, stroke=1)
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=82, optimize=True)
        buf.seek(0)
        c.drawImage(ImageReader(buf), x, y, width=dw, height=dh, preserveAspectRatio=True, mask="auto")
        c.showPage()
        print("OK", idx, item["code"], item["path"])

    # ===== APPENDIX: leftover files scanned =====
    c.setFillColorRGB(*DARK)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColorRGB(*PINK)
    c.setFont("Times-Bold", 18)
    c.drawString(25 * mm, h - 25 * mm, "Folder scan appendix")
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica", 10)
    c.drawString(25 * mm, h - 40 * mm, f"Sequenced unique assets in this PDF: {len(pages)}")
    c.drawString(25 * mm, h - 50 * mm, f"Other files found under images/ + drawings/ (duplicates or extras): {len(leftovers)}")
    y = h - 65 * mm
    c.setFillColorRGB(*MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(25 * mm, y, "Extras / duplicates not given a separate sheet (already covered by hash or superseded by images/):")
    y -= 8 * mm
    c.setFillColorRGB(*GOLD)
    for name in leftovers[:40]:
        c.drawString(28 * mm, y, f"· {name}")
        y -= 5 * mm
        if y < 20 * mm:
            break
    if len(leftovers) > 40:
        c.drawString(28 * mm, y, f"… +{len(leftovers) - 40} more")
    c.showPage()

    c.save()
    shutil.copy2(OUT, OUT_COPY)
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1024 / 1024:.1f} MB) pages_assets={len(pages)}")
    print(f"leftovers={len(leftovers)}")


if __name__ == "__main__":
    build()
