from gc import collect
from pathlib import Path
from time import time_ns
from typing import cast

from memory_profiler import memory_usage
from numpy import array, float64, ndarray

from methods import convert_pdf_to_cmyk_tiff_custom, convert_pdf_to_cmyk_tiff_gs
from plotting import Graph, Plot, PlotType, graph

CWD: Path = Path(__file__).parent.resolve()
GPATH: Path = CWD / "examples"
GPATH.mkdir(parents=True, exist_ok=True)
PATTERNS = CWD / "patterns"
PATTERNS.mkdir(parents=True, exist_ok=True)
IMAGES = CWD / "images"
IMAGES.mkdir(parents=True, exist_ok=True)
RUNS = 60


pdfs = [_ for _ in PATTERNS.glob("*.pdf")]
xaxis = array([i for i in range(RUNS)], order="C", dtype=float64)

for pdf in pdfs:
    custom_times = ndarray(RUNS, order="C", dtype=float64)
    custom_memory_max = ndarray(RUNS, order="C", dtype=float64)
    # custom_memory_std = ndarray(RUNS, order="C", dtype=float64)

    gs_times = ndarray(RUNS, order="C", dtype=float64)
    gs_memory_max = ndarray(RUNS, order="C", dtype=float64)
    # gs_memory_std = ndarray(RUNS, order="C", dtype=float64)

    for index in range(RUNS):
        print(f"Processing CUSTOM {pdf.name} @ {pdf} - Run {index + 1}")
        now = time_ns()

        mems = array(
            memory_usage(
                (
                    convert_pdf_to_cmyk_tiff_custom,
                    (pdf, IMAGES / f"{pdf.name}_custom.png"),
                    {},
                ),
                interval=0.25,
                timeout=5,
            ),
            dtype=float64,
        )

        elapsed = time_ns() - now
        custom_times[index] = elapsed / 1000000
        custom_memory_max[index] = mems.max()
        collect()

    for index in range(RUNS):
        print(f"Processing GS {pdf.name} @ {pdf} - Run {index + 1}")
        now = time_ns()

        mems = array(
            memory_usage(
                (
                    convert_pdf_to_cmyk_tiff_gs,
                    (pdf, IMAGES / f"{pdf.name}_gs.png"),
                    {},
                ),
                interval=0.25,
                timeout=5,
            ),
            dtype=float64,
        )

        elapsed = time_ns() - now
        gs_times[index] = elapsed / 1000000
        gs_memory_max[index] = mems.max()
        collect()

    custom_times_plot = cast(
        Plot,
        {
            "label": f"PDF {pdf.name} CUSTOM {pdf.stat().st_size / 1024:.2f} KB",
            "x": xaxis,
            "y": custom_times.copy(order="C"),
            "type": PlotType.LINE,
            "size": 5,
            "approximation": None,
        },
    )

    gs_times_plot = cast(
        Plot,
        {
            "label": f"PDF {pdf.name} GS {pdf.stat().st_size / 1024:.2f} KB",
            "x": xaxis,
            "y": gs_times.copy(order="C"),
            "type": PlotType.LINE,
            "size": 5,
            "approximation": None,
        },
    )

    custom_memory_plot = cast(
        Plot,
        {
            "label": f"PDF {pdf.name} CUSTOM {pdf.stat().st_size / 1024:.2f} KB",
            "x": xaxis,
            "y": custom_memory_max.copy(order="C"),
            "type": PlotType.LINE,
            "size": 5,
            "approximation": None,
        },
    )

    gs_memory_plot = cast(
        Plot,
        {
            "label": f"PDF {pdf.name} GS {pdf.stat().st_size / 1024:.2f} KB",
            "x": xaxis,
            "y": gs_memory_max.copy(order="C"),
            "type": PlotType.LINE,
            "size": 5,
            "approximation": None,
        },
    )

    times_graph = cast(
        Graph,
        {
            "name": f"{pdf.name}_times",
            "title": f"PDF {pdf.name} TIMES",
            "x_label": "Runs",
            "y_label": "Time (ms)",
            "fontsize": 10,
            "plots": [
                custom_times_plot,
                gs_times_plot,
            ],
        },
    )

    memory_graph = cast(
        Graph,
        {
            "name": f"{pdf.name}_memory",
            "title": f"PDF {pdf.name} MEMORY",
            "x_label": "Runs",
            "y_label": "Memory (KB)",
            "fontsize": 10,
            "plots": [
                custom_memory_plot,
                gs_memory_plot,
            ],
        },
    )

    graph(times_graph, GPATH / f"{pdf.name}_times.png")
    graph(memory_graph, GPATH / f"{pdf.name}_memory.png")
