# EJL Lighthouse — Development execution guide

Plain-text guide (no code blocks). Use with the development-order PDF.

**Main PDF:** download/EJL-Lighthouse-development-order.pdf  
**Gallery:** index.html  
**Full memo:** ARCHITECTURE-AND-COST.md

---

## How to execute (phases 0–9)

**Phase 0 — Brand & brief**  
Lock EJL pink/gold identity before any FF&E orders.

**Phase 1 — Design intent**  
Freeze fountain, fireplace, pole, rooftop atmosphere (concept images 10–14, 20–21).

**Phase 2 — Guest journey / ops**  
Define journey G-01, payment P-01 (electronic only, no tips), robot routing R-01, branding B-01.

**Phase 3 — Building shell & MEP**  
Section A-03 and MEP schematic M-01. Civil Defense pre-consult for coal exhaust, HVAC, fire.

**Phase 4 — Spatial plans**  
Freeze indoor A-01 and rooftop A-02 footprints. Clear robot aisles ≥1.2 m, stretcher ≥1.1 m.

**Phase 5 — Kitchen / BOH**  
Build prep, cook, dish, cold/dry stores, robot loading bay, dumbwaiter (A-08).

**Phase 6 — Safety & staff**  
Emergency room A-05 and staff rest/changing A-06 with closets C01–C12.

**Phase 7 — VIP-1 (indoor)**  
Principal suite A-04: lounge + office + bedroom + ensuite, e-locked.

**Phase 8 — VIP-2 (rooftop)**  
Terrace add-on A-07 after VIP-1 lessons. Replaces 8 rooftop seats when booked.

**Phase 9 — Procurement & opening**  
FF&E schedule F-01, vendor orders, staff training, soft open.

---

## PDF downloads

| File | Purpose |
|------|---------|
| EJL-Lighthouse-development-order.pdf | Every image + definition in build order |
| EJL-Lighthouse-all-images.pdf | All sheets A4 landscape |
| EJL-Lighthouse-A1-boards.pdf | Key plans print-ready |
| dubai-hookah-lounge-drawings.zip | SVG plans + JPEG images + PDFs |

---

## Rebuild PDFs

From repository root, run:

- python3 docs/dubai-hookah-lounge/scripts/build-development-order-pdf.py
- python3 docs/dubai-hookah-lounge/scripts/build-all-images-pdf.py

---

## Folder scan (what was included)

- images/ — 30 concept PNGs (00, 10–29)
- drawings/ — plan SVGs + logo
- Duplicates in drawings/ (classic-* and *-concept.png copies) are covered by images/ in the development-order PDF

Only extra file not given its own PDF sheet: drawings/ejl-lighthouse-logo.svg (PNG logo already included).
