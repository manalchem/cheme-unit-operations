# ChemE Balance Calculator

A command-line Python tool for solving **steady-state mass and energy balances** across common chemical engineering unit operations. Built as a portfolio project to demonstrate core ChemE fundamentals programmatically.

---

## Unit Operations Included

| # | Unit Operation | Balance Type | Key Concept |
|---|---------------|-------------|-------------|
| 1 | Mixing Tank | Mass balance (multi-component) | ṁ₁ + ṁ₂ = ṁ_out |
| 2 | Conversion Reactor (A → B) | Mass balance with reaction | Species balance + fractional conversion |
| 3 | Shell & Tube Heat Exchanger | Energy balance | Q_hot = Q_cold |

---

## How to Run

**Requirements:** Python 3.10+, no external libraries needed.

```bash
# Clone the repository
git clone https://github.com/manalmahamat/cheme-unit-operations.git

# Run the program
python balance_calculator.py
```

You'll see an interactive menu:

```
  ╔══════════════════════════════════════════════════╗
  ║        ChemE Balance Calculator  v1.0           ║
  ║   Mass & Energy Balances for Unit Operations    ║
  ╚══════════════════════════════════════════════════╝

  Select a unit operation:
    [1]  Mixing Tank          (mass balance)
    [2]  Conversion Reactor   (mass balance, A→B)
    [3]  Heat Exchanger       (energy balance)
    [q]  Quit
```

---

## Sample Output

### Mixing Tank
```
  Enter Stream 1 conditions:
    Total flow rate (kg/hr): 100
    Mass fraction of component A (0-1): 0.30

  Enter Stream 2 conditions:
    Total flow rate (kg/hr): 50
    Mass fraction of component A (0-1): 0.60

  ── Results ────────────────────────────────────────
  Outlet total flow rate              150.0000  kg/hr
  Outlet mass fraction A                0.4000  —
  Outlet mass flow of A                60.0000  kg/hr
  Outlet mass flow of B (solvent)      90.0000  kg/hr

  ── Mass Balance Verification ──────────────────────
  Total mass IN                       150.0000  kg/hr
  Total mass OUT                      150.0000  kg/hr
  ✓  Balance satisfied (error < 0.01 %)
```

### Conversion Reactor
```
  Enter feed stream conditions:
    Total feed flow rate (kg/hr): 200
    Mass fraction of reactant A in feed (0-1): 0.80
    Mass fraction of product B in feed  (0-1): 0.00
    Fractional conversion of A (0-1): 0.75

  ── Results ────────────────────────────────────────
  Reactant A consumed                 120.0000  kg/hr
  Unreacted A in outlet                40.0000  kg/hr
  Product B in outlet                 120.0000  kg/hr
  Inert in outlet                      40.0000  kg/hr
  Total outlet flow                   200.0000  kg/hr
  Outlet mass fraction A                0.2000  —
  Outlet mass fraction B                0.6000  —

  ✓  Balance satisfied (error < 0.01 %)
```

### Heat Exchanger
```
  Hot-side stream:
    Mass flow rate (kg/hr): 500
    Heat capacity Cp (kJ/kg·K): 4.18
    Inlet temperature (°C): 90
    Outlet temperature (°C): 60

  Cold-side stream:
    Mass flow rate (kg/hr): 300
    Heat capacity Cp (kJ/kg·K): 4.18
    Inlet temperature (°C): 20

  ── Results ────────────────────────────────────────
  Duty Q  (transferred)             62700.0000  kJ/hr
  Duty Q  (transferred)                17.4167  kW
  Cold fluid ΔT                        50.0000  K
  Cold outlet temperature              70.0000  °C
  Hot-side ΔT                          30.0000  K

  ✓  Energy balance satisfied
```

---

## Engineering Concepts Applied

- **Law of Conservation of Mass** — total mass in = total mass out at steady state
- **Species / Component Balances** — tracking individual components through a system
- **Fractional Conversion** — X = moles reacted / moles fed (applied on mass basis)
- **Enthalpy Balance** — Q = ṁ · Cp · ΔT for sensible heat transfer
- **Input Validation** — thermodynamic feasibility checks on all outputs

---

## Project Background

Built as part of a chemical engineering portfolio while completing prerequisite coursework at Northern Virginia Community College, ahead of transfer to a four-year ChemE program. The goal was to bridge early coursework (stoichiometry, thermodynamics fundamentals) with practical programming skills.

---

## Planned Additions

- [ ] Distillation column (multicomponent VLE)
- [ ] Pipe flow pressure drop calculator (Darcy-Weisbach)
- [ ] Matplotlib-generated process flow diagrams
- [ ] Unit conversion utilities (SI ↔ Imperial)
- [ ] Export results to CSV

---

## Author

**Manal**
Chemical Engineering Student | Northern Virginia Community College
