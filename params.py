import pathlib
import matplotlib
import numpy as np


repoPath = pathlib.Path.cwd()
root = pathlib.Path(r"C:\data\monkey-data")
figPath = repoPath / "figures"
LargeFig = (7, 8)
MedFig = (4.3, 4.3)

from monkey import defs as monkey_defs

rng = np.random.default_rng(np.random.SeedSequence(12345))
n_iter = 100


def set_rc_params(dictArg: dict = {}):
    matplotlib.rcParams["backend"] = "PDF"
    matplotlib.rcParams["lines.markersize"] = 4
    matplotlib.rcParams["xtick.major.pad"] = 1
    matplotlib.rcParams["ytick.major.pad"] = 1
    matplotlib.rcParams["axes.labelpad"] = 2
    matplotlib.rcParams["axes.titlepad"] = 5
    matplotlib.rcParams["font.size"] = 8
    matplotlib.rcParams["axes.titlesize"] = 8
    matplotlib.rcParams["axes.labelsize"] = 8
    matplotlib.rcParams["xtick.labelsize"] = 6.5
    matplotlib.rcParams["ytick.labelsize"] = 6.5
    matplotlib.rcParams["legend.fontsize"] = 6.5
    matplotlib.rcParams["legend.title_fontsize"] = 6.5
    matplotlib.rcParams["text.usetex"] = True
    matplotlib.rcParams["font.family"] = "sans-serif"
    matplotlib.rcParams["font.serif"] = "Helvetica"
    matplotlib.rcParams["legend.frameon"] = False
    matplotlib.rcParams["legend.fancybox"] = False
    matplotlib.rcParams["figure.dpi"] = 600

    for key, val in dictArg.items():
        matplotlib.rcParams[key] = val


class panels:
    "sizes of different panels in the paper"

    TinyH = 0.5
    SmallH = 1.2
    MedH = SmallH + TinyH
    BigH = 3

    schmatic = (2, MedH)
    raster = (2.4, SmallH)
    velocity = (LargeFig[0] - schmatic[0], TinyH)
    proj_3d_align = (LargeFig[0], SmallH)
    cca = (1.5, SmallH)
    cca_hist = (2, SmallH)

    rnn_raster = (2, SmallH)
    rnn_velocity = (2, TinyH)
    rnn_cca = (1.5, MedH - 0.2)
    rnn_cca_hist = (2, MedH - 0.2)


class colors:
    "colors for different data types in the paper"

    MouseM1 = "tab:blue"
    MouseStr = "tab:orange"
    MainCC = "r"
    LowerCC = "k"
    UpperCC = "cornflowerblue"
    Sim1CC = "cornflowerblue"
    Sim2CC = "palevioletred"
    SimAcrossCC = "indigo"
    MonkeyPts = "xkcd:brown"
    MousePts = "xkcd:violet"
    LeftTrial = (0, 1, 0, 1)
    RightTrial = (1, 0, 0, 1)
