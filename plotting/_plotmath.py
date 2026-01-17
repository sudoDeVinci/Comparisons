from numpy import array, float64, log2, polyfit
from numpy.typing import NDArray

from ._structs import Plot, PlotType


def linear_regression(
    x: NDArray[float64], y: NDArray[float64]
) -> tuple[float, float, float]:
    """
    Calculate and return the slope, intercept and linear regression coefficient
    from the x and y values passed in.
    """

    n = len(x)

    x_bar = sum(x) / n
    y_bar = sum(y) / n

    slope = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(x, y)) / sum(
        (xi - x_bar) ** 2 for xi in x
    )

    intercept = y_bar - slope * x_bar

    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x_sq = sum(xi**2 for xi in x)
    sum_y_sq = sum(yi**2 for yi in y)

    r_numer = n * sum_xy - sum_x * sum_y
    r_denom = ((n * sum_x_sq - sum_x**2) * (n * sum_y_sq - sum_y**2)) ** 0.5
    r_value = r_numer / r_denom if r_denom > 0 else 0

    return slope, intercept, r_value


def power_law(x: NDArray[float64], y: NDArray[float64]) -> tuple[float, float, float]:
    """
    Calculate power-law eqn for a given set of x and y values.
    Return in the form [slope, intercept, coefficient]
    """
    log_x: NDArray[float64] = log2(x, dtype=float)
    log_y: NDArray[float64] = log2(y, dtype=float)

    slope, intercept, r_value = linear_regression(log_x, log_y)

    return slope, 2**intercept, r_value


def generate_expected_data(
    slope: float,
    intercept: float,
    x: NDArray[float64],
    plot_type: PlotType,
    eq: str,
    size: int,
) -> Plot | None:
    """
    Generate expected values for a given list of values for an independent variable
    according to the type of plot.
    """
    plot: Plot | None = None

    match plot_type:
        case PlotType.LINEAR:
            plot = Plot(
                label=f"Linear Approx. {eq}", x=x, type=PlotType.LINE, size=size
            )
            plot["y"] = array(
                [(slope * x_val) + intercept for x_val in x], dtype=float64
            )
            plot["approximation"] = None

        case PlotType.EXPONENTIAL:
            plot = Plot(label=f"Exp. Approx. {eq}", x=x, type=PlotType.LINE, size=size)
            plot["y"] = array(
                [intercept * (x_val**slope) for x_val in x], dtype=float64
            )
            plot["approximation"] = None

        case PlotType.LOGARITHMIC:
            plot = Plot(label=f"Log. Approx. {eq}", x=x, type=PlotType.LINE, size=size)
            plot["y"] = array(
                [intercept * (x_val**slope) for x_val in x], dtype=float64
            )
            plot["approximation"] = None

        case _:
            plot = None

    return plot
