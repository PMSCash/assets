# EJL Lighthouse — Architecture, Robot Ops & Cost

**House name:** **EJL Lighthouse** (Dubai)  
**Brand:** Flashy **pink + gold** · logo on all robots, VIP plaques, and app  
**Concept:** 50-seat premium rooftop + indoor lounge  
**Offer:** Electronic hookah + traditional coal shisha (Russian / Turkish / Arabic) + dining  
**Service model:** Table-delivery robots; orders routed digitally → kitchen → robot → table  
**Payments:** **Strictly electronic · no cash · no tipping · donations only** (optional, separate from bill)  
**Drawings:** see [`drawings/`](./drawings/), [`index.html`](./index.html), and [`download/`](./download/) zip pack

---

## 1. Seat & zone program

| Zone | Seats | Notes |
|------|------:|-------|
| Rooftop lounge | 28 | Pergola, reflective linear ceiling lighting, e-shisha OK |
| Indoor dining | 10 | Food-led, robot-primary aisles |
| Indoor e-shisha lounge | 4 | Electronic only, odor extract |
| **VIP suite** | **8–10** | **E-locked · indoor fountain · fireplace · pole dance · TVs/VOD · hostesses** |
| Coal shisha room | *(capacity within 50 via booth rotation; design for ~10 booth seats)* | **Negative pressure, staff-only, no robots** |
| Massage seats | 6 | Within indoor footprint (shared with lounge dwell) |
| **Emergency / seizure room** | — | **On-site first-response medical room (non-seating)** |
| **Design total** | **50** | Rooftop 28 + indoor 22 (VIP counted in indoor) |

**Assumed net area:** ~370–440 m² (indoor + rooftop usable + emergency room), excluding MEP plant.

---

## 2. Robot architecture (table delivery)

### Fleet
| Unit | Role |
|------|------|
| R1–R3 | Indoor dining + e-shisha lounge delivery · **EJL pink/gold logo tagged** |
| R4 | Rooftop delivery from bar handoff · **same EJL livery** |
| + docks | 1 indoor charging dock, 1 rooftop charging point |

**Robot branding:** Circular **EJL** mark (pink + gold) on front panel; **EJL LIGHTHOUSE** wordmark on both sides; tray liners carry mini logo. See [`drawings/08-robot-branding.svg`](./drawings/08-robot-branding.svg) and [`drawings/ejl-lighthouse-logo.svg`](./drawings/ejl-lighthouse-logo.svg).

### Order path
1. Guest orders via **QR / table tablet** (VIP: VOD pad / app)
2. **POS** stamps table ID + zone (INDOOR / ROOF / VIP)
3. **Kitchen Display (KDS)** tickets food/drink
4. Staff plates tray at **Robot Loading Bay**
5. System assigns free robot → SLAM path to table
6. Guest takes tray → robot returns → dock/charge
7. Guest settles via **electronic pay only** → optional **donation** prompt (never a tip)

### Hard rules
- Robots **never enter coal shisha room**
- Robots **never enter VIP suite** while e-door is locked — trays stop at **service pass**
- Robots do **not** carry hot coals or lit traditional pipes
- Robots have **no payment slot** (pay is table / VIP / host terminal only)
- Traditional coal service = **staff only** through airlock vestibule
- Fountain, stairs, coal vestibule, VIP suite, **emergency room** = **virtual walls** in robot map
- Main aisle clear width ≥ **1.2 m**; stretcher path to emergency room / exit ≥ **1.1 m**

### Rooftop mode (recommended)
Kitchen → **service lift / dumbwaiter tray** → rooftop bar handoff → **R4** → table  
*(Keeps robots level-bound; simpler for Civil Defense / lift approvals.)*

### Budget for robotics (see cost section)
- Hardware: 4 delivery robots + docks  
- Software: POS + KDS + robot fleet manager + QR menus  
- Mapping / integration / training  

---

## 2.1 Payment system — strictly electronic

| Rule | Spec |
|------|------|
| Cash | **Not accepted** anywhere (tables, bar, VIP, host stand) |
| Tipping | **Disabled** — no tip line on POS, tablet, or receipt; staff cannot accept tip gifts |
| Bill | Itemized F&B + VAT only; optional house **service fee** (if used) must be a fixed % disclosed up front — **not** a tip |
| Tender | Card contactless · Apple / Google / Samsung Pay · UAE wallets / QR |
| Touchpoints | Host NFC · table QR · VIP NFC + VOD pad pay |
| After pay | E-receipt to phone → optional **donation** screen |
| Donations | **Only** voluntary electronic gift to a designated **house fund or partner charity** — never routed to an individual staffer |
| Staff pay | Salary / wage model only — **no tip pool** |
| Audit | All payments and donations logged; offline / unlogged guest pay forbidden |

See drawing [`drawings/07-payment-system.svg`](./drawings/07-payment-system.svg) (P-01).

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
| **VIP suite (e-closed)** | Private ~50 m²; e-lock; **indoor fountain · fireplace · pole dance**; 3 TVs + VOD; hostesses |
| **Emergency / seizure room** | ~18 m² first-response room: treatment bed, O2, suction, AED, seizure kit, stretcher, EMS route |
| **EJL brand system** | Pink (#FF2D95 / #FF69B4) + gold (#D4AF37) · logo on robots, VIP plaque, app, tray liners |

### 4.1 VIP suite — fountain, fireplace, pole + hostess + TVs

| Item | Spec |
|------|------|
| Capacity | 8–10 guests |
| Door | Flush electronic door; magnetic lock (~600 kg); fail-safe open on fire alarm; LED LOCKED status |
| Access | RFID / booking app unlock; hostess can badge guests in |
| Privacy | Vestibule sound lock; door remains closed for the booking window |
| **Indoor fountain** | Feature fountain with pink LED wash; waterproofing + drain; guest keep-clear ring |
| **Fireplace** | Gas fireplace with gold surround + guard; Civil Defense–compliant flue / sealed unit |
| **Pole dance** | Chrome pole on circular stage; pink uplight; soft floor; **2.4 m clear height** |
| **Displays** | **1× 75" main wall TV + 2× 55" side TVs**; matrix switcher; mirror or solo modes |
| **On-demand** | Guest **VOD pad** on low table; sports / film / karaoke catalogs; no lobby CCTV feed into suite |
| AV rack | Streaming players + scene lighting control in suite AV closet |
| Service | 2 VIP hostesses (greeting, ordering aid, e-shisha assist, media assist, privacy etiquette) |
| Pay | In-room NFC + VOD pad — **electronic only**; hostesses **cannot** take tips or cash |
| F&B path | Robot → corridor stop → **service pass window** → hostess handoff inside |
| Smoke | E-shisha only inside VIP (no coal) |
| Panic | In-suite panic → FOH + **emergency room** + EMS call |
| Add-on CAPEX | Fit-out AED 450k–1.1M (incl. fountain/fireplace/pole); e-lock AED 40k–120k; **TVs + VOD AED 80k–220k** |
| Hostess OPEX | AED 18k–40k / month (2 FTE equivalent, shift cover) |

### 4.2 On-site emergency / seizure treatment room

Designed as a **first-response medical room** for seizure / collapse / hypoxia stabilization until EMS arrives — not a hospital ER. Stocking prescription meds requires **DHA clinic / pharmacy pathway**.

| Item | Spec |
|------|------|
| Area | ~18 m², adjacent to staff / guest WC, near VIP corridor |
| Bed | Treatment bed with padded side rails; soft floor zone for fall protection |
| Airway / O2 | Oxygen cylinder + regulator; portable suction |
| Cardiac | Wall AED with monthly check log |
| Seizure kit | Timing clock, gloves, bite protection per protocol, first-aid; meds only if licensed |
| Transfer | Folding stretcher park; clear EMS route to lift / street |
| Call system | Panic buttons from VIP + FOH linked to room + **998** / private ambulance |
| Posted protocol | Protect → Time → Recovery position → Airway → EMS if &gt;5 min / injury / first seizure |
| Staffing | Trained first-aiders every shift; optional on-call nurse on peak VIP nights |
| CAPEX | Fit-out AED 80k–220k + equipment AED 40k–120k |
| OPEX | Training / consumables / nurse cover AED 3k–12k / month |

**Hard rules:** robots never park or route through the emergency room; stretcher path kept clear; privacy curtain for guest dignity.

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
| **VIP suite fit-out + e-lock + fountain/fireplace/pole** | **450k–900k** | **800k–1.5M** |
| **VIP TVs + on-demand AV** | **80k–180k** | **150k–280k** |
| **EJL brand livery (robots + suite plaques + print)** | **25k–80k** | **50k–140k** |
| **Emergency / seizure room + kit** | **120k–280k** | **200k–400k** |
| Hookah equipment (coal + e-shisha) | 120k–500k | 250k–900k |
| Kitchen / commissary | 400k–1.3M | 800k–2.4M |
| **Robots + POS/KDS/QR integration** | **250k–550k** | **450k–1.1M** |
| **E-pay terminals + no-tip POS config + donation flow** | **40k–120k** | **80k–200k** |
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
| Staff (FOH + kitchen + shisha + VIP hostesses + supervisor) | 98k–200k |
| First-aid / optional nurse cover + medical consumables | 3k–12k |
| Utilities (HVAC-heavy) | 25k–60k |
| Consumables (tobacco, coals, e-liquid, F&B) | 40k–100k |
| VIP VOD / streaming licenses | 1k–5k |
| Payment gateway / POS SaaS (no-tip build) | 1k–4k |
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
| [`drawings/05-vip-room-plan.svg`](./drawings/05-vip-room-plan.svg) | **A-04 VIP suite:** fountain · fireplace · pole · e-lock · TVs · hostess |
| [`drawings/06-emergency-room-plan.svg`](./drawings/06-emergency-room-plan.svg) | **A-05 Emergency / seizure room:** bed, O2, AED, EMS route |
| [`drawings/07-payment-system.svg`](./drawings/07-payment-system.svg) | **P-01 Payment:** electronic only · no tip · donations only |
| [`drawings/08-robot-branding.svg`](./drawings/08-robot-branding.svg) | **B-01 Robot livery:** EJL pink/gold logo on fleet |
| [`drawings/ejl-lighthouse-logo.svg`](./drawings/ejl-lighthouse-logo.svg) | **Brand logo** (SVG) |
| [`drawings/ejl-lighthouse-logo.png`](./drawings/ejl-lighthouse-logo.png) | **Brand logo** (PNG) |
| [`drawings/01-rooftop-concept.png`](./drawings/01-rooftop-concept.png) | Rooftop atmosphere concept |
| [`drawings/02-indoor-robot-concept.png`](./drawings/02-indoor-robot-concept.png) | Indoor robot + fountain concept |
| [`drawings/03-building-section-concept.png`](./drawings/03-building-section-concept.png) | Section concept render |
| [`drawings/04-vip-room-concept.png`](./drawings/04-vip-room-concept.png) | Earlier VIP concept |
| [`drawings/05-vip-ejl-concept.png`](./drawings/05-vip-ejl-concept.png) | **EJL VIP concept:** fountain · fireplace · pole · pink/gold |
| [`download/dubai-hookah-lounge-drawings.zip`](./download/dubai-hookah-lounge-drawings.zip) | **Full image set** (all PNG + SVG) for download |

Open [`index.html`](./index.html) for a single-page drawing board.

---

## 8. Next professional steps (Dubai)

1. Engage licensed architect + MEP consultant familiar with **shisha / F&B** approvals  
2. Confirm **landlord NOC** for coal exhaust stacks and rooftop loads  
3. Civil Defense pre-consult on coal room negative pressure + fire strategy  
4. DTCM / municipality licensing path for lounge + dining concept  
5. Robot vendor site survey after preliminary FF&E freeze  
6. Confirm **DHA / first-aid** pathway for on-site seizure room (clinic license only if stocking meds)  
7. Spec VIP **VOD / IPTV** vendor + content licensing for private suites  
8. Configure POS / gateway with **tip fields removed** and optional **donation** destination (charity / house fund)  

---

*Concept package only — not construction documents. All costs are indicative ranges for planning.*
