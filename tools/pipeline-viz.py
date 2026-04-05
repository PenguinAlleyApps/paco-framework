#!/usr/bin/env python3
"""PA·co Pipeline Visualizer — ASCII DAG of product phase transitions.

Reads state/PIPELINE.md and outputs an ASCII directed acyclic graph showing
where each product sits in the 7-phase workflow.

Usage:
    python tools/pipeline-viz.py                     # auto-detect PIPELINE.md
    python tools/pipeline-viz.py state/PIPELINE.md   # explicit path
    python tools/pipeline-viz.py --compact            # minimal output
    python tools/pipeline-viz.py --history            # include completed/killed

Built by PA·co — A Penguin Alley System (penguinalley.com)
"""

import re
import sys
from pathlib import Path

# 7-phase workflow in order
PHASES = [
    ("RESEARCH", "Research"),
    ("REFINE", "Refine"),
    ("POST_REFINE", "Post-Refine"),
    ("CEO_GATE", "CEO Gate"),
    ("DEVELOP", "Develop"),
    ("DEPLOY", "Deploy"),
    ("EVOLVE", "Evolve"),
]

# Map raw PIPELINE.md phase strings to canonical phase keys
PHASE_ALIASES = {
    "RESEARCH": "RESEARCH",
    "REFINE": "REFINE",
    "POST_REFINE": "POST_REFINE",
    "POST-REFINE": "POST_REFINE",
    "PENDING_CEO": "CEO_GATE",
    "CEO_GATE": "CEO_GATE",
    "CEO GATE": "CEO_GATE",
    "APPROVED": "DEVELOP",
    "DEVELOP": "DEVELOP",
    "READY_FOR_FINAL_QA": "DEVELOP",
    "READY_FOR_DEPLOY": "DEPLOY",
    "DEPLOYED_PENDING_CEO": "DEPLOY",
    "DEPLOY": "DEPLOY",
    "EVOLVE": "EVOLVE",
    "EVOLVE_A": "EVOLVE",
    "EVOLVE_B": "EVOLVE",
    "EVOLVE_C": "EVOLVE",
    "EVOLVE_D": "EVOLVE",
}

# Status indicators
INDICATOR = {
    "active": "\u25cf",      # ● filled circle
    "blocked": "\u25d0",     # ◐ half circle
    "pending": "\u25cb",     # ○ empty circle
    "completed": "\u2713",   # ✓ check
    "killed": "\u2717",      # ✗ cross
}


def find_pipeline(explicit_path=None):
    """Locate PIPELINE.md by searching common locations."""
    if explicit_path:
        p = Path(explicit_path)
        if p.exists():
            return p
        print(f"Error: {explicit_path} not found", file=sys.stderr)
        sys.exit(1)

    candidates = [
        Path("state/PIPELINE.md"),
        Path("PIPELINE.md"),
        Path("../state/PIPELINE.md"),
    ]
    for c in candidates:
        if c.exists():
            return c

    print("Error: PIPELINE.md not found. Pass path as argument.", file=sys.stderr)
    sys.exit(1)


def parse_pipeline(path):
    """Parse PIPELINE.md into structured product data."""
    text = path.read_text(encoding="utf-8")
    products = {"active": [], "develop": [], "completed": [], "killed": []}
    week_mode = "UNKNOWN"

    # Extract week mode
    mode_match = re.search(r"mode:\s*(\w+)", text)
    if mode_match:
        week_mode = mode_match.group(1)

    # Parse markdown tables
    current_section = None
    for line in text.splitlines():
        lower = line.lower().strip()
        # Only detect section headers (lines starting with ##)
        if line.strip().startswith("##") or line.strip().startswith("#"):
            if "active products" in lower:
                current_section = "active"
            elif "in development" in lower:
                current_section = "develop"
            elif "completed" in lower:
                current_section = "completed"
            elif "killed" in lower:
                current_section = "killed"
            elif "queued" in lower or "accumulated" in lower:
                current_section = None
                continue

        if current_section and line.strip().startswith("|") and "---" not in line and "Product" not in line:
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 3 and cols[0].strip():
                name = cols[0].strip()
                phase_raw = cols[1].strip()
                status = cols[2].strip() if len(cols) > 2 else ""
                phase_key = PHASE_ALIASES.get(phase_raw, None)

                # Try partial match if exact match fails
                if not phase_key:
                    for alias, key in PHASE_ALIASES.items():
                        if alias in phase_raw.upper():
                            phase_key = key
                            break

                if phase_key:
                    # Determine indicator
                    status_lower = status.lower()
                    if "block" in status_lower or "pending_ceo" in status_lower or "awaiting" in status_lower:
                        ind = INDICATOR["blocked"]
                    elif current_section == "completed":
                        ind = INDICATOR["completed"]
                    elif current_section == "killed":
                        ind = INDICATOR["killed"]
                    else:
                        ind = INDICATOR["active"]

                    products[current_section].append({
                        "name": name,
                        "phase": phase_key,
                        "phase_raw": phase_raw,
                        "status": status[:60],
                        "indicator": ind,
                    })

    return products, week_mode


def render_dag(products, week_mode, compact=False, show_history=False):
    """Render the ASCII DAG."""
    lines = []

    # Header
    lines.append("PA\u00b7co Pipeline DAG")
    lines.append(f"Week: {week_mode}")
    lines.append("")

    # Build phase boxes
    box_width = 12
    phase_boxes = []
    for key, label in PHASES:
        padded = label.center(box_width)
        phase_boxes.append((key, padded))

    # Top border
    top = "  ".join(f"\u250c{'─' * box_width}\u2510" for _, _ in phase_boxes)
    mid = "──\u25b6 ".join(f"\u2502{p}\u2502" for _, p in phase_boxes)
    bot = "  ".join(f"\u2514{'─' * box_width}\u2518" for _, _ in phase_boxes)
    arrow_row = "  ".join(" " * (box_width + 2) for _ in phase_boxes)

    lines.append(top)
    lines.append(mid)
    lines.append(bot)
    lines.append("")

    # Map products to phases
    phase_products = {key: [] for key, _ in PHASES}
    all_products = products["active"] + products["develop"]
    if show_history:
        all_products += products.get("completed", []) + products.get("killed", [])

    for prod in all_products:
        if prod["phase"] in phase_products:
            phase_products[prod["phase"]].append(prod)

    # Find max products in any phase for row count
    max_in_phase = max((len(v) for v in phase_products.values()), default=0)

    if max_in_phase > 0:
        # Render product rows under their phase columns
        for row_idx in range(max_in_phase):
            cells = []
            for key, _ in PHASES:
                prods = phase_products[key]
                if row_idx < len(prods):
                    p = prods[row_idx]
                    label = f"{p['indicator']} {p['name']}"
                    # Truncate to fit column
                    if len(label) > box_width + 2:
                        label = label[:box_width - 1] + "\u2026"
                    cells.append(label.center(box_width + 2))
                else:
                    cells.append(" " * (box_width + 2))
            lines.append("".join(cells))

        lines.append("")

    # Legend
    lines.append("Legend:")
    lines.append(f"  {INDICATOR['active']} Active    {INDICATOR['blocked']} Blocked/Awaiting    {INDICATOR['pending']} Pending")
    if show_history:
        lines.append(f"  {INDICATOR['completed']} Completed    {INDICATOR['killed']} Killed")
    lines.append("")

    # Product detail table (unless compact)
    if not compact and all_products:
        lines.append("Products:")
        name_width = max(len(p["name"]) for p in all_products)
        for p in all_products:
            phase_label = dict(PHASES).get(p["phase"], p["phase_raw"])
            lines.append(f"  {p['indicator']} {p['name']:<{name_width}}  {phase_label:<12}  {p['status']}")

    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    compact = "--compact" in args
    show_history = "--history" in args
    path_arg = None

    for a in args:
        if not a.startswith("--"):
            path_arg = a

    pipeline_path = find_pipeline(path_arg)
    products, week_mode = parse_pipeline(pipeline_path)
    output = render_dag(products, week_mode, compact=compact, show_history=show_history)
    print(output)


if __name__ == "__main__":
    import io, os
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
