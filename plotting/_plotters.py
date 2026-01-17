from typing import Callable

from matplotlib.axes import Axes

from ._plotmath import generate_expected_data, linear_regression, power_law
from ._structs import Equation, ExpEq, LineEq, LogEq, Plot, PlotType


def _line(ax: Axes, plot: Plot) -> None:
    """
    Plot a line and give it a label.
    """
    label: str = f"{plot['label']}" if plot["label"] != "None" else "Plot data"
    ax.plot(plot["x"], plot["y"], label=label, linewidth=str(plot["size"]))


def _scatter(ax: Axes, plot: Plot) -> None:
    """
    Plot a scatter plot and give it a label.
    """

    label: str = f"{plot['label']}" if plot["label"] != "None" else "Plot data"
    ax.scatter(plot["x"], plot["y"], s=plot["size"] * 2, alpha=0.8, label=label)


def _approximated(ax: Axes, plot: Plot) -> None:
    """
    Plot scatterpoints, then find and plot the approximated equation of them.
    """

    expected_plot = get_graph_data(plot)

    _scatter(ax, plot)
    if expected_plot is not None:
        expected_plot["label"] = f"{plot['label']} {expected_plot['label']}"
        _line(ax, expected_plot)

    # print(f">> Actual plot: {str(plot)[:100]} ...")
    # print(f">> Expected plot: {str(expected_plot)[:100]} ... \n")


def _do_nothing(ax: Axes, plot: Plot) -> None:
    """
    Do absolutely nothing.
    """
    pass


def get_graph_data(inPlot: Plot) -> Plot | None:
    """
    Get the approximate function and Plot for a set off data as a tuple.
    Args:
        inPlot (Plot): The input plot data.

    Returns:
        Plot | None: The approximate function and Plot for the input data.
    """

    equation: Equation | None = None
    x_coords = inPlot["x"]
    y_coords = inPlot["y"]
    type = inPlot["type"]

    match type:
        case PlotType.LINEAR:
            slope, intercept, r_value = linear_regression(x_coords, y_coords)
            equation = LineEq(r_value, intercept, slope)

        case PlotType.EXPONENTIAL:
            slope, intercept, r_value = power_law(x_coords, y_coords)
            equation = ExpEq(r_value, intercept, slope)

        case PlotType.LOGARITHMIC:
            slope, intercept, r_value = power_law(x_coords, y_coords)
            equation = LogEq(r_value, intercept, slope)

        case _:
            equation = None
            slope = None
            intercept = None

    # Generate expected values
    expected_data = (
        generate_expected_data(
            equation.slope,
            equation.intercept,
            x_coords,
            type,
            equation.equation,
            max(inPlot["size"] // 10, 1),
        )
        if equation is not None
        else None
    )

    return expected_data


def get_plotter(plot: Plot) -> Callable[[Axes, Plot], None]:
    """
    Return the plotting function corresponding to the graph type.
    """
    plotFunc: Callable = _do_nothing

    match plot["type"]:
        case PlotType.LINEAR | PlotType.LOGARITHMIC | PlotType.EXPONENTIAL:
            plotFunc = _approximated
        case PlotType.LINE:
            plotFunc = _line
        case PlotType.SCATTER:
            plotFunc = _scatter
        case PlotType.NONE:
            plotFunc = _do_nothing

    return plotFunc
