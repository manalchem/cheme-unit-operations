"""
=============================================================
 ChemE Balance Calculator
 Mass & Energy Balance Tool for Common Unit Operations
=============================================================
 Author: Manal
 Description:
   An interactive command-line tool for solving steady-state
   mass and energy balances across three unit operations:
     1. Mixing Tank       — mass balance, multi-component
     2. Conversion Reactor — mass balance with reaction
     3. Heat Exchanger    — energy balance, hot/cold streams

 Usage:
   Run from terminal:  python balance_calculator.py
   Select a unit operation from the main menu.
=============================================================
"""

# ── Imports ──────────────────────────────────────────────────────────────────
import sys


# ── Utilities ─────────────────────────────────────────────────────────────────
def print_header(title: str) -> None:
    """Print a formatted section header."""
    width = 56
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_result(label: str, value: float, unit: str) -> None:
    """Print a single result line with consistent formatting."""
    print(f"  {label:<35} {value:>10.4f}  {unit}")


def get_float(prompt: str, min_val: float = None) -> float:
    """
    Prompt the user for a float value with optional minimum validation.

    Parameters
    ----------
    prompt  : str   — Text shown to the user
    min_val : float — If provided, reject values below this threshold

    Returns
    -------
    float — Validated user input
    """
    while True:
        try:
            val = float(input(f"  {prompt}: "))
            if min_val is not None and val < min_val:
                print(f"  ⚠  Value must be ≥ {min_val}. Try again.")
                continue
            return val
        except ValueError:
            print("  ⚠  Please enter a valid number.")


def mass_balance_check(inputs: list[float], outputs: list[float]) -> None:
    """
    Verify that total mass in ≈ total mass out and print the result.

    Parameters
    ----------
    inputs  : list of flow rates entering the system  (kg/hr)
    outputs : list of flow rates leaving the system   (kg/hr)
    """
    total_in  = sum(inputs)
    total_out = sum(outputs)
    error_pct = abs(total_in - total_out) / total_in * 100 if total_in else 0

    print("\n  ── Mass Balance Verification ──────────────────────")
    print_result("Total mass IN",  total_in,  "kg/hr")
    print_result("Total mass OUT", total_out, "kg/hr")
    if error_pct < 0.01:
        print("  ✓  Balance satisfied (error < 0.01 %)")
    else:
        print(f"  ✗  Balance error: {error_pct:.4f} %  — check inputs")


# ── Unit Operation 1: Mixing Tank ─────────────────────────────────────────────
def mixing_tank() -> None:
    """
    Steady-state mass balance for a mixing tank with two inlet streams.

    Governing equation (overall):
        ṁ₁ + ṁ₂ = ṁ_out

    Component balance for solute A:
        ṁ₁·x₁ + ṁ₂·x₂ = ṁ_out·x_out
        → x_out = (ṁ₁·x₁ + ṁ₂·x₂) / ṁ_out
    """
    print_header("UNIT OPERATION 1 — Mixing Tank")
    print("""
   Stream 1 ──┐
              ├──► Mixed Output
   Stream 2 ──┘

  Two streams mix at steady state.
  We calculate the outlet flow rate and composition.
    """)

    # ── Inputs ────────────────────────────────────────────────────────────────
    print("  Enter Stream 1 conditions:")
    m1 = get_float("  Total flow rate (kg/hr)", min_val=0)
    x1 = get_float("  Mass fraction of component A  (0 – 1)", min_val=0)

    print("\n  Enter Stream 2 conditions:")
    m2 = get_float("  Total flow rate (kg/hr)", min_val=0)
    x2 = get_float("  Mass fraction of component A  (0 – 1)", min_val=0)

    # ── Calculations ──────────────────────────────────────────────────────────
    m_out  = m1 + m2                              # overall balance
    x_out  = (m1 * x1 + m2 * x2) / m_out         # component balance
    mA_out = m_out * x_out                        # mass flow of A out
    mB_out = m_out * (1 - x_out)                  # mass flow of B out

    # ── Results ───────────────────────────────────────────────────────────────
    print("\n  ── Results ────────────────────────────────────────")
    print_result("Outlet total flow rate",          m_out,         "kg/hr")
    print_result("Outlet mass fraction A",          x_out,         "—")
    print_result("Outlet mass flow of A",           mA_out,        "kg/hr")
    print_result("Outlet mass flow of B (solvent)", mB_out,        "kg/hr")

    mass_balance_check([m1, m2], [m_out])


# ── Unit Operation 2: Conversion Reactor ──────────────────────────────────────
def conversion_reactor() -> None:
    """
    Steady-state mass balance for a single-stream CSTR or PFR
    with a simple irreversible reaction:

        A  →  B          (stoichiometry 1:1, equal molecular weights assumed)

    Governing equations:
        ṁ_A,out = ṁ_A,in · (1 − X)
        ṁ_B,out = ṁ_B,in + ṁ_A,in · X        (product generated)
        ṁ_total,out = ṁ_A,out + ṁ_B,out + ṁ_inert
    """
    print_header("UNIT OPERATION 2 — Conversion Reactor  (A → B)")
    print("""
  Feed ──► [ REACTOR ] ──► Product stream

  Reaction:  A  →  B   (irreversible, 1:1 molar ratio)
  Assumes equal molecular weights for A and B (mass basis).
    """)

    # ── Inputs ────────────────────────────────────────────────────────────────
    print("  Enter feed stream conditions:")
    m_total = get_float("  Total feed flow rate (kg/hr)",             min_val=0)
    xA_in   = get_float("  Mass fraction of reactant A in feed (0–1)", min_val=0)
    xB_in   = get_float("  Mass fraction of product B in feed  (0–1)", min_val=0)
    X       = get_float("  Fractional conversion of A  (0–1)",         min_val=0)

    # Validate fractions
    if xA_in + xB_in > 1.0:
        print("  ⚠  xA + xB > 1. Remainder treated as inert.")
    x_inert = max(0.0, 1.0 - xA_in - xB_in)

    # ── Calculations ──────────────────────────────────────────────────────────
    mA_in    = m_total * xA_in
    mB_in    = m_total * xB_in
    m_inert  = m_total * x_inert

    mA_rxn   = mA_in * X                        # mass of A reacted
    mA_out   = mA_in - mA_rxn                   # unreacted A leaving
    mB_out   = mB_in + mA_rxn                   # product B leaving
    m_out    = mA_out + mB_out + m_inert         # total outlet

    # ── Results ───────────────────────────────────────────────────────────────
    print("\n  ── Results ────────────────────────────────────────")
    print_result("Reactant A consumed",     mA_rxn,              "kg/hr")
    print_result("Unreacted A in outlet",   mA_out,              "kg/hr")
    print_result("Product B in outlet",     mB_out,              "kg/hr")
    print_result("Inert in outlet",         m_inert,             "kg/hr")
    print_result("Total outlet flow",       m_out,               "kg/hr")
    print_result("Outlet mass fraction A",  mA_out / m_out,      "—")
    print_result("Outlet mass fraction B",  mB_out / m_out,      "—")

    mass_balance_check([m_total], [m_out])


# ── Unit Operation 3: Heat Exchanger ──────────────────────────────────────────
def heat_exchanger() -> None:
    """
    Steady-state energy balance for a shell-and-tube heat exchanger
    (no phase change, no heat loss to surroundings).

    Governing equation:
        Q = ṁ_hot · Cp_hot · (T_hot,in − T_hot,out)
          = ṁ_cold · Cp_cold · (T_cold,out − T_cold,in)

    Given: hot side fully specified → solve for cold outlet temperature
           (or vice versa — user chooses unknown).
    """
    print_header("UNIT OPERATION 3 — Shell & Tube Heat Exchanger")
    print("""
  Hot fluid  ──► [  HX  ] ──► Cooled hot fluid
  Cold fluid ◄── [      ] ◄── Heated cold fluid

  Energy balance (no phase change, adiabatic shell):
      Q_hot  = Q_cold
      ṁ_h·Cp_h·ΔT_h = ṁ_c·Cp_c·ΔT_c
    """)

    # ── Inputs ────────────────────────────────────────────────────────────────
    print("  Hot-side stream:")
    m_hot    = get_float("  Mass flow rate (kg/hr)",                 min_val=0)
    Cp_hot   = get_float("  Heat capacity Cp  (kJ / kg·K)",         min_val=0)
    T_hot_in = get_float("  Inlet temperature (°C)")
    T_hot_out= get_float("  Outlet temperature (°C)")

    print("\n  Cold-side stream:")
    m_cold    = get_float("  Mass flow rate (kg/hr)",                min_val=0)
    Cp_cold   = get_float("  Heat capacity Cp  (kJ / kg·K)",        min_val=0)
    T_cold_in = get_float("  Inlet temperature (°C)")

    # ── Calculations ──────────────────────────────────────────────────────────
    Q_hot      = m_hot * Cp_hot * (T_hot_in - T_hot_out)   # kJ/hr
    dT_cold    = Q_hot / (m_cold * Cp_cold)                 # K
    T_cold_out = T_cold_in + dT_cold

    # Sanity checks
    if T_hot_out >= T_hot_in:
        print("\n  ⚠  Warning: Hot outlet ≥ hot inlet — check direction.")
    if T_cold_out > T_hot_in:
        print("\n  ⚠  Warning: Cold outlet exceeds hot inlet — thermodynamically impossible.")

    # ── Results ───────────────────────────────────────────────────────────────
    print("\n  ── Results ────────────────────────────────────────")
    print_result("Duty Q  (transferred)",    Q_hot,          "kJ/hr")
    print_result("Duty Q  (transferred)",    Q_hot / 3600,   "kW")
    print_result("Cold fluid ΔT",            dT_cold,        "K")
    print_result("Cold outlet temperature",  T_cold_out,     "°C")
    print_result("Hot-side ΔT",              T_hot_in - T_hot_out, "K")

    print("\n  ── Energy Balance Verification ─────────────────────")
    Q_cold = m_cold * Cp_cold * dT_cold
    print_result("Q_hot  (heat released)",   Q_hot,  "kJ/hr")
    print_result("Q_cold (heat absorbed)",   Q_cold, "kJ/hr")
    if abs(Q_hot - Q_cold) < 1e-6:
        print("  ✓  Energy balance satisfied")
    else:
        print(f"  ✗  Balance error: {abs(Q_hot - Q_cold):.6f} kJ/hr")


# ── Main Menu ──────────────────────────────────────────────────────────────────
def main() -> None:
    """Entry point — display menu and route to selected unit operation."""

    banner = r"""
  ╔══════════════════════════════════════════════════╗
  ║        ChemE Balance Calculator  v1.0           ║
  ║   Mass & Energy Balances for Unit Operations    ║
  ╚══════════════════════════════════════════════════╝
    """
    print(banner)

    menu = {
        "1": ("Mixing Tank          (mass balance)",        mixing_tank),
        "2": ("Conversion Reactor   (mass balance, A→B)",   conversion_reactor),
        "3": ("Heat Exchanger       (energy balance)",      heat_exchanger),
        "q": ("Quit",                                        None),
    }

    while True:
        print("\n  Select a unit operation:")
        for key, (desc, _) in menu.items():
            print(f"    [{key}]  {desc}")

        choice = input("\n  Enter choice: ").strip().lower()

        if choice == "q":
            print("\n  Goodbye!\n")
            sys.exit(0)
        elif choice in menu:
            _, fn = menu[choice]
            fn()
            input("\n  Press Enter to return to the main menu...")
        else:
            print("  ⚠  Invalid choice. Please enter 1, 2, 3, or q.")


if __name__ == "__main__":
    main()
