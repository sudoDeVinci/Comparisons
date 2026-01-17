# Comparison Plotting Utility

## Description  
A lightweight Python library for creating comparison plots from numeric data.  
It supports linear, exponential, logarithmic, and scatter plots, and can automatically compute and overlay best‑fit curves.  
Designed for quick visual comparison of multiple data series in a single image.

Features

- **Multiple plot types**: Linear, Exponential, Logarithmic, Scatter, and straight line.
- **Automatic regression**: Computes linear or power‑law fit and draws the approximation.
- **Customizable styling**: Set point size, line width, font size, and labels.
- **Extensible**: Add new plot types by extending the `PlotType` enum and the `get_plotter` dispatcher.

```python
from pathlib import Path
from typing import cast

from numpy import array

from plotting import Graph, PlotType, graph

CWD: Path = Path(__file__).parent.resolve()
GPATH: Path = CWD / "examples"
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
                "x": array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float),
                "y": array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float),
                "type": PlotType.LINEAR,
                "size": 10,
            },
            {
                "label": "Data 2",
                "x": array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float),
                "y": array(
                    [
                        1,
                        1.5,
                        1.75,
                        1.875,
                        1.9375,
                        1.96875,
                        1.984375,
                        1.9921875,
                        1.99609375,
                        1.998046875,
                    ],
                    dtype=float,
                ),
                "type": PlotType.LOGARITHMIC,
                "size": 10,
            },
            {
                "label": "Data 3",
                "x": array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=float),
                "y": array(
                    [0.03125, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8],
                    dtype=float,
                ),
                "type": PlotType.EXPONENTIAL,
                "size": 10,
            },
        ],
        "fontsize": 12,
    },
)

graph(graphobj, GPATH / "graph.png")
```
