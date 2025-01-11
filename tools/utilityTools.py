import matplotlib.pyplot as plt
import numpy as np
import os, time
from functools import wraps


def phantom_axes(ax):
    "Make an axes invisible"
    ax.set_xticks([])
    ax.set_yticks([])
    [ax.spines[key].set_visible(False) for key in ax.spines.keys()]
    ax.set_facecolor("None")
    ax.set_alpha(0)
    return ax


def get_colors(n, colormap="plasma"):
    colors = []
    cmap = plt.cm.get_cmap(colormap)
    for colorVal in np.linspace(0, 1, n + 1):
        colors.append(cmap(colorVal))
    return colors[:-1]


def find_file(path, extension=[".raw.kwd"]):
    """
    This function finds all the file types specified by 'extension' (ex: *.dat) in the 'path' directory
    and all its subdirectories and their sub-subdirectories etc.,
    and returns a list of all file paths
    'extension' is a list of desired file extensions: ['.dat','.prm']
    """
    if isinstance(extension, str):
        extension = (
            extension.split()
        )  # turning extension into a list with a single element
    return [
        os.path.join(walking[0], goodfile)
        for walking in list(os.walk(path))
        for goodfile in walking[2]
        for ext in extension
        if goodfile.endswith(ext)
    ]


def shaded_errorbar(
    ax: plt.axes,
    x: np.array,
    y: np.array = None,
    lineStat=np.mean,
    errorStat=np.std,
    alpha=0.2,
    **props,
):
    """
    ax: axis to plot into
    x,y: data, solumns in y are collapsed to calculate the errorbar
    lineStat: a function to measure the midline, must accept an `axis` argument
    errorStat: a function to measure the  symmetric errorbars, must accept an `axis` argument
    most other keyword arguments will be passed to `plt.fill_between` and *some* to `plt.plot`
    """
    if y is None:
        y = x
        x = np.arange(y.shape[0])

    line = ax.plot(x, lineStat(y, axis=1))[0]

    shadeProps = props.copy()
    for key in props.keys():
        if key == "color" or key == "c":
            line.set_color(props[key])
        elif key == "linewidth" or key == "lw":
            line.set_linewidth(props[key])
        elif key == "linestyle" or key == "ls":
            line.set_linestyle(props[key])
        elif key == "marker":
            line.set_marker(props[key])
            shadeProps.pop(key, None)
        elif key == "markersize" or key == "ms":
            line.set_markersize(props[key])
            shadeProps.pop(key, None)
        elif key == "label":
            line.set_label(props[key])
            shadeProps.pop(key, None)

    shadedY = errorStat(y, axis=1)
    shade = ax.fill_between(
        x,
        lineStat(y, axis=1) - shadedY,
        lineStat(y, axis=1) + shadedY,
        alpha=alpha,
        **shadeProps,
    )

    return line, shade


def plot_targets(ax=None, markerSize=50):
    if ax is None:
        ax = plt.figure(figsize=(5, 5)).add_subplot(1, 1, 1, fc="None")

    x = [np.cos(i * np.pi / 4) for i in range(8)]
    y = [np.sin(i * np.pi / 4) for i in range(8)]
    c = get_colors(8)
    ax.scatter(x=x, y=y, c=c, s=markerSize, marker="o")
    ax.set_axis_off()
    return ax


def add_gridspec_abs(
    fig,
    nrows=1,
    ncols=1,
    left=0,
    bottom=0,
    right=None,
    top=None,
    width=1,
    height=1,
    **kwargs,
):
    """
    Equivalent to `fig.add_gridspec` except  all the inputs are in absolute values in inches.
    """
    figw, figh = fig.get_size_inches()
    if right is None or top is None:  # aligned on bottom left
        gs = fig.add_gridspec(
            nrows=nrows,
            ncols=ncols,
            left=left / figw,
            bottom=bottom / figh,
            right=(left / figw) + (width / figw),
            top=(bottom / figh) + (height / figh),
            **kwargs,
        )
    else:  # aligned on top right
        gs = fig.add_gridspec(
            nrows=nrows,
            ncols=ncols,
            left=(right / figw) - (width / figw),
            bottom=(top / figh) - (height / figh),
            right=right / figw,
            top=top / figh,
            **kwargs,
        )

    return gs


def report(func):
    "decorator to print the name and execution time of the function being executed."

    @wraps(func)
    def inner(*ar, **kar):
        print(f"Running: `{func.__name__}`...", end="\r")
        start = time.time()
        out = func(*ar, **kar)
        print(f"Executed: `{func.__name__}` in {time.time() - start:.1f}s")
        return out

    return inner
