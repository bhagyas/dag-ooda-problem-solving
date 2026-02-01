#!/usr/bin/env -S uv run --with networkx --
"""
DAG + OODA helper: read nodes/edges (JSON), optional weights; output order, sources, longest path, recommended first.
Input: stdin or file. JSON: {"nodes": [...], "edges": [[a,b],...], "weights": {"id": {"impact": 4, "effort": 2}}}
"""
import json
import sys
from pathlib import Path

import networkx as nx

DEFAULT_IMPACT = 3
DEFAULT_EFFORT = 3


def score(impact: int | float, effort: int | float) -> float:
    """Priority score: impact / effort. Effort 0 treated as 1."""
    e = effort if effort >= 1 else 1
    return impact / e


def main() -> None:
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        data = json.loads(path.read_text())
    else:
        data = json.load(sys.stdin)

    nodes = data.get("nodes", [])
    edges = [tuple(e) for e in data.get("edges", [])]
    weights_map = data.get("weights", {})

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    if not nx.is_directed_acyclic_graph(G):
        print("ERROR: Graph has a cycle. Break cycles before proceeding.", file=sys.stderr)
        sys.exit(1)

    order = list(nx.topological_sort(G))
    sources = [n for n in G.nodes() if G.in_degree(n) == 0]
    try:
        longest = nx.dag_longest_path(G)
    except Exception:
        longest = []

    def get_impact_effort(node: str) -> tuple[float, float]:
        w = weights_map.get(node, {})
        imp = w.get("impact", DEFAULT_IMPACT)
        eff = w.get("effort", DEFAULT_EFFORT)
        return float(imp), float(eff)

    source_scores = []
    for n in sources:
        imp, eff = get_impact_effort(n)
        source_scores.append((n, imp, eff, score(imp, eff)))
    recommended = max(source_scores, key=lambda x: x[3])[0] if source_scores else ""

    print("TOPOLOGICAL_ORDER")
    for n in order:
        print(n)
    print("SOURCES")
    for n in sources:
        print(n)
    print("LONGEST_PATH")
    for n in longest:
        print(n)
    print("SOURCE_SCORES")
    for n, imp, eff, sc in source_scores:
        print(f"{n}\timpact={imp}\teffort={eff}\tscore={sc:.2f}")
    print("RECOMMENDED_FIRST")
    print(recommended)


if __name__ == "__main__":
    main()
