"""Cell 4: compare the map's import arrows with the import graph that pydeps finds.

From the notebook: %run compare_map.py pydeps payment_job --max-bacon 0. It adds --show-deps --no-output,
so pydeps prints the graph as text and draws nothing.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check import LAB, graph_arrows, map_arrows, show  # noqa: E402


def compare(command: list[str]) -> None:
    """Print each arrow that is in only one of the map and the graph."""
    if command[:2] != ["pydeps", "payment_job"]:
        print('Type the command in cell 4 first: command = "pydeps payment_job --max-bacon 0". See step 5.')
        return
    graph = graph_arrows(command[1:])
    codemap = LAB / "CODEMAP.md"
    arrows = map_arrows(codemap.read_text(encoding="utf-8")) if codemap.is_file() else set()
    print("Arrows in the graph:", len(graph))
    print("In the map, not in the graph:", show(arrows - graph))
    print("In the graph, not in the map:", show(graph - arrows))


if __name__ == "__main__":
    compare(sys.argv[1:])
