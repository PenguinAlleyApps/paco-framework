# Pipeline Visualization

> Visualize your product pipeline as an ASCII directed acyclic graph (DAG).

## Overview

PA·co's 7-phase workflow is a linear pipeline with branching at Evolve (multiple products can be in Evolve simultaneously). The `pipeline-viz.py` tool reads your `state/PIPELINE.md` and renders an ASCII DAG showing where each product sits.

## Usage

```bash
# Auto-detect PIPELINE.md in state/ directory
python tools/pipeline-viz.py

# Explicit path
python tools/pipeline-viz.py state/PIPELINE.md

# Compact mode (no product detail table)
python tools/pipeline-viz.py --compact

# Include completed and killed products
python tools/pipeline-viz.py --history
```

## Example Output

```
PA·co Pipeline DAG
Week: SPRINT

┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
│  Research  │──▶│   Refine   │──▶│Post-Refine │──▶│  CEO Gate  │──▶│  Develop   │──▶│   Deploy   │──▶│   Evolve   │
└────────────┘  └────────────┘  └────────────┘  └────────────┘  └────────────┘  └────────────┘  └────────────┘

                                                ◐ NewProduct                     ● ProductA
                                                                                 ● ProductB

Legend:
  ● Active    ◐ Blocked/Awaiting    ○ Pending
```

## Status Indicators

| Symbol | Meaning | When |
|--------|---------|------|
| ● | Active | Product is progressing normally |
| ◐ | Blocked/Awaiting | Waiting for CEO decision or external input |
| ○ | Pending | Queued but not started |
| ✓ | Completed | Successfully launched (with `--history`) |
| ✗ | Killed | Terminated (with `--history`) |

## Phase Mapping

The tool maps various status strings from `PIPELINE.md` to the 7 canonical phases:

| PIPELINE.md Value | Mapped Phase |
|---|---|
| `RESEARCH` | Research |
| `REFINE` | Refine |
| `POST_REFINE` | Post-Refine |
| `PENDING_CEO`, `CEO_GATE` | CEO Gate |
| `APPROVED`, `DEVELOP`, `READY_FOR_FINAL_QA` | Develop |
| `READY_FOR_DEPLOY`, `DEPLOYED_PENDING_CEO` | Deploy |
| `EVOLVE_A` through `EVOLVE_D` | Evolve |

## Integration with Schedules

Add pipeline visualization to your standup or weekly report schedule:

```markdown
# In your standup schedule script:
python tools/pipeline-viz.py --compact
```

This gives agents a quick visual snapshot of where all products stand before starting their session.

## How It Differs from LangGraph

LangGraph provides runtime visualization of agent execution graphs (nodes = functions, edges = transitions). PA·co's pipeline visualization shows the **product lifecycle** (nodes = workflow phases, products = entities moving through phases). This is a higher-level view: not "how does one agent think" but "where are all our products in the development pipeline."

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
- `state/PIPELINE.md` in the expected markdown table format (see [state-schema.md](../core/state-schema.md))
