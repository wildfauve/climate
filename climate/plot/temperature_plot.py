import matplotlib.pyplot as plt
import matplotlib.path as mpath
import numpy as np
from matplotlib.lines import Line2D

from climate import dataframe

markers = Line2D.filled_markers

def locale_temperatures(df):
    _create_plot("_temp/temps.png",df, days=df.columns[1:])


def _create_plot(file, df, days):
    np_arr = df.to_numpy()

    fig, ax = _plot_figure("Days", days)

    for locale_temps in np_arr:
        ax.plot(days, locale_temps[1:], label=locale_temps[0], marker=_to_marker(locale_temps[0]))

    ax.set_ylabel('Temperature Celsius')  # Add a y-label to the axes.
    ax.set_title("Min Max Temperature @ Locale")  # Add a title to the axes.
    ax.legend(bbox_to_anchor=(1.1, 1.05), fancybox=True, shadow=True)  # Add a legend.
    fig.savefig(file)


def _plot_figure(name, days):
    fig, ax = plt.subplots(figsize=(15, 7), layout='constrained')
    ax.set_xticks(range(0, len(days)))
    ax.set_xticklabels(days)
    ax.set_xlabel(name)  # Add an x-label to the axes.
    return fig, ax


def _to_marker(locale):
    return markers[hash(locale) % 16]


def _markers2():
    star = mpath.Path.unit_regular_star(6)
    circle = mpath.Path.unit_circle()
    # concatenate the circle with an internal cutout of the star
    cut_star = mpath.Path(
        vertices=np.concatenate([circle.vertices, star.vertices[::-1, ...]]),
        codes=np.concatenate([circle.codes, star.codes]))

    return {'star': star, 'circle': circle, 'cut_star': cut_star}
