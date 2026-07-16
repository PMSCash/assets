# Dubai Premium Hookah Lounge — Architecture, Robot Ops & Cost

**Concept:** 50-seat premium rooftop + indoor lounge in Dubai  
**Offer:** Electronic hookah + traditional coal shisha (Russian / Turkish / Arabic) + dining  
**Service model:** Table-delivery robots; orders routed digitally → kitchen → robot → table  
**Drawings:** see [`drawings/`](./drawings/) and [`index.html`](./index.html)

---

## 1. Seat & zone program

| Zone | Seats | Notes |
|------|------:|-------|
| Rooftop lounge | 28 | Pergola, reflective linear ceiling lighting, e-shisha OK |
| Indoor dining | 14 | Food-led, robot-primary aisles |
| Indoor e-shisha lounge | 8 | Electronic only, odor extract |
| Coal shisha room | *(capacity within 50 via booth rotation; design for ~10 booth seats)* | **Negative pressure, staff-only, no robots** |
| Massage seats | 6 | Within indoor footprint (shared with lounge dwell) |
| **Design total** | **50** | Rooftop 28 + indoor 22 |

**Assumed net area:** ~350–420 m² (indoor + rooftop usable), excluding MEP plant.

---

## 2. Robot architecture (table delivery)

### Fleet
| Unit | Role |
|------|------|
| R1–R3 | Indoor dining + e-shisha lounge delivery |
| R4 | Rooftop delivery from bar handoff |
| + docks | 1 indoor charging dock, 1 rooftop charging point |

### Order path
1. Guest orders via **QR / table tablet**
2. **POS** stamps table ID + zone (INDOOR / ROOF)
3. **Kitchen Display (KDS)** tickets food/drink
4. Staff plates tray at **Robot Loading Bay**
5. System assigns free robot → SLAM path to table
6. Guest takes tray → robot returns → dock/charge

### Hard rules
- Robots **never enter coal shisha room**
- Robots do **not** carry hot coals or lit traditional pipes
- Traditional coal service = **staff only** through airlock vestibule
- Fountain, stairs, coal vestibule = **virtual walls** in robot map
- Main aisle clear width ≥ **1.2 m**

### Rooftop mode (recommended)
Kitchen → **service lift / dumbwaiter tray** → rooftop bar handoff → **R4** → table  
*(Keeps robots level-bound; simpler for Civil Defense / lift approvals.)*

### Budget for robotics (see cost section)
- Hardware: 4 delivery robots + docks  
- Software: POS + KDS + robot fleet manager + QR menus  
- Mapping / integration / training  

---

## 3. Smoke & MEP strategy

```
[Dining / e-shisha]  ← make-up air
        ↓ pressure cascade
[Airlock vestibule]
        ↓
[Coal room NEGATIVE] → dedicated exhaust duct → ROOF STACKS
```

- Separate AHU/exhaust for coal room  
- Dining return air **not** shared with coal exhaust  
- Fire detection + fan interlocks per Civil Defense  
- Coal bar with enclosed ember handling + metal ash bins  

---

## 4. Signature features

| Feature | Design intent |
|---------|----------------|
| Rooftop ceiling lighting | Linear reflective strips under pergola (luxury automotive-inspired look; no brand logos) |
| Indoor fountain | Central calm anchor; waterproofing + drain + 0.8 m robot keep-out |
| Massage seats | 6 powered seats; quiet zone lighting; service power + maintenance access |
| Premium dining | Limited kitchen/commissary; robot-led FOH |

---

## 5. CAPEX cost model (Dubai, AED)

Ranges assume a **premium** fit-out in a suitable rooftop-capable building. Landlord shell condition, location grade (Marina / DIFC / Downtown / Business Bay), and authority conditions swing totals.

### Total project bands
| Tier | Total CAPEX (AED) | Notes |
|------|------------------:|-------|
| Premium | **10M – 16M** | Strong finishes + full coal exhaust + 4 robots |
| Ultra-premium | **16M – 28M** | Heavier rooftop structure, fountain, lighting, brand FF&E |

≈ **AED 200k – 560k per seat** depending on tier and shell condition.

### Breakdown (indicative)

| Category | Premium (AED) | Ultra (AED) |
|----------|-------------:|------------:|
| Design + engineering (arch/MEP/FF&E) | 200k–500k | 400k–900k |
| Permits / Civil Defense / authority | 250k–900k | 450k–1.3M |
| Rooftop waterproofing + structure | 300k–1.4M | 700k–2.8M |
| HVAC + coal dedicated exhaust | 1.4M–3.2M | 2.8M–6.0M |
| Fire safety systems | 300k–1.0M | 550k–1.7M |
| Electrical + ceiling lighting feature | 600k–1.8M | 1.2M–3.2M |
| Fountain plumbing + waterproofing | 150k–550k | 300k–1.0M |
| Interior fit-out | 1.6M–3.8M | 3.2M–7.0M |
| Furniture + massage seats | 350k–1.4M | 900k–2.2M |
| Hookah equipment (coal + e-shisha) | 120k–500k | 250k–900k |
| Kitchen / commissary | 400k–1.3M | 800k–2.4M |
| **Robots + POS/KDS/QR integration** | **250k–550k** | **450k–1.1M** |
| IT / CCTV / networking | 60k–220k | 140k–480k |
| Contingency | 12%–20% | 15%–25% |

### Robot line item detail (typical)
| Item | Qty | Unit (AED) | Subtotal |
|------|----:|----------:|---------:|
| Indoor delivery robots | 3 | 45k–90k | 135k–270k |
| Rooftop delivery robot | 1 | 45k–90k | 45k–90k |
| Charging docks | 2 | 8k–15k | 16k–30k |
| Fleet software + mapping | 1 | 25k–80k | 25k–80k |
| POS + KDS + QR menus | 1 | 30k–80k | 30k–80k |
| Integration / training | 1 | 20k–60k | 20k–60k |
| **Robotics subtotal** | | | **~270k–610k** |

---

## 6. OPEX snapshot (monthly, rough)

| Item | AED / month |
|------|------------:|
| Rent (highly location-dependent) | 150k–450k+ |
| Staff (FOH + kitchen + shisha + supervisor) | 80k–160k |
| Utilities (HVAC-heavy) | 25k–60k |
| Consumables (tobacco, coals, e-liquid, F&B) | 40k–100k |
| Robot maintenance / SaaS | 3k–10k |
| Marketing | 15k–40k |

---

## 7. Drawing index

| File | Content |
|------|---------|
| [`drawings/01-indoor-floor-plan.svg`](./drawings/01-indoor-floor-plan.svg) | Indoor plan: dining, fountain, massage, kitchen, robot bay, coal room |
| [`drawings/02-rooftop-floor-plan.svg`](./drawings/02-rooftop-floor-plan.svg) | Rooftop plan: 28 seats, bar handoff, exhaust stacks |
| [`drawings/03-robot-routing.svg`](./drawings/03-robot-routing.svg) | Order lifecycle + indoor path loops + rooftop handoff |
| [`drawings/04-section-elevation.svg`](./drawings/04-section-elevation.svg) | Cut section: levels, exhaust, fountain, robots |
| [`drawings/01-rooftop-concept.png`](./drawings/01-rooftop-concept.png) | Rooftop atmosphere concept |
| [`drawings/02-indoor-robot-concept.png`](./drawings/02-indoor-robot-concept.png) | Indoor robot + fountain concept |
| [`drawings/03-building-section-concept.png`](./drawings/03-building-section-concept.png) | Section concept render |

Open [`index.html`](./index.html) for a single-page drawing board.

---

## 8. Next professional steps (Dubai)

1. Engage licensed architect + MEP consultant familiar with **shisha / F&B** approvals  
2. Confirm **landlord NOC** for coal exhaust stacks and rooftop loads  
3. Civil Defense pre-consult on coal room negative pressure + fire strategy  
4. DTCM / municipality licensing path for lounge + dining concept  
5. Robot vendor site survey after preliminary FF&E freeze  

---

*Concept package only — not construction documents. All costs are indicative ranges for planning.*
