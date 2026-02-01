# DAG + OODA Problem-Solving

Uses **NetworkX** DAGs and **OODA** (Observe, Orient, Decide, Act) to derive the best course of action for fixing or solving new problems. Use when you face a new bug, feature, or decision and want a structured plan, dependency-ordered tasks, or a repeatable problem-solving workflow.

## Overview

- **OODA**: Observe → Orient → Decide → Act (Boyd’s loop).
- **DAG**: Directed acyclic graph of tasks; edges = dependencies (A must be done before B).
- **Output**: Topological order, sources (first actions), longest path, and a recommended first step (impact/effort scoring).

## Requirements

- Python 3.10+
- [NetworkX](https://networkx.org/) (installed automatically with `uv` or `pip`)

## Quick Start

### 1. Run the helper script (recommended)

From the repo root, with [uv](https://github.com/astral-sh/uv) (no venv needed):

```bash
uv run --with networkx python scripts/ooda_dag.py
```

Then paste JSON and press Ctrl-D, or pass a file:

```bash
uv run --with networkx python scripts/ooda_dag.py path/to/dag.json
```

**JSON format:**

```json
{
  "nodes": ["fix-auth", "add-retry", "deploy", "update-docs"],
  "edges": [
    ["fix-auth", "deploy"],
    ["add-retry", "deploy"],
    ["deploy", "update-docs"]
  ],
  "weights": {
    "fix-auth": { "impact": 5, "effort": 2 },
    "add-retry": { "impact": 3, "effort": 1 }
  }
}
```

- `nodes`: list of task IDs.
- `edges`: list of `[from, to]` pairs (prerequisite → dependent).
- `weights` (optional): per-node `impact` (1–5) and `effort` (1–5). Defaults: 3, 3.

**Output:** `TOPOLOGICAL_ORDER`, `SOURCES`, `LONGEST_PATH`, `SOURCE_SCORES`, and `RECOMMENDED_FIRST`. Exit code 1 if the graph has a cycle.

### 2. Use as a Cursor/Codex skill

Copy this repo (or symlink) into your skills directory (e.g. `~/.cursor/skills/dag-ooda-problem-solving`). The `SKILL.md` in the root describes when and how agents should use the DAG + OODA workflow and the script.

## Workflow (from SKILL.md)

1. **Observe**: List all tasks/fixes/sub-problems (nodes).
2. **Orient**: Add dependencies (edges), build the DAG, ensure it’s acyclic.
3. **Decide**: Topological sort; optionally score sources by impact/effort and pick the best first action.
4. **Act**: Execute the chosen step; re-Observe and update the DAG as needed.

## License

MIT. See [LICENSE](LICENSE).
