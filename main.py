from pathlib import Path
from typing import cast

from numpy import array

from pyplot import Graph, PlotType, graph

CWD: Path = Path(__file__).parent.resolve()
GPATH: Path = CWD / "graphs"
GPATH.mkdir(parents=True, exist_ok=True)

graphobj = cast(
    Graph,
    {
        "name": "Comparison Graph",
        "title": "Comparison Graph",
        "x_label": "X-axis",
        "y_label": "Y-axis",
        "plots": [
            {
                "label": "Data 1",
                "x": array([1, 2, 3, 4, 5], dtype=float),
                "y": array([1, 2, 3, 4, 5], dtype=float),
                "type": PlotType.LINEAR,
                "size": 10,
            },
            {
                "label": "Data 2",
                "x": array([2, 4, 6, 8, 10], dtype=float),
                "y": array([1, 2, 3, 4, 5], dtype=float),
                "type": PlotType.LINEAR,
                "size": 10,
            },
        ],
        "fontsize": 12,
    },
)

graph(graphobj, GPATH / "graph.png")
