from typing import List
from pathlib import Path

# import seaborn as sns
# import plotly.express as px

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pendulum
import polars as pl
from matplotlib.lines import Line2D

from clojos_common.util import monad

markers = Line2D.filled_markers

temp_file_root = Path("_temp")

TITLE = "Min Max Temperature @ Locale"
X_TITLE = "Recorded For 24 Hour Period (~0800 Recorded For Day -> ~0800 Day + 1)"
Y_TITLE = "Temperate (Celsius)"



def locale_temperatures(df):
    return monad.Right(_create_plot(_file(), df))


def _file():
    return temp_file_root / f"locale_daily_temperature_{pendulum.now().to_date_string()}.png"

def _create_plot(file, df):
    dates = _unique_recorded_for(df)
    locales = _unique_locales(df)

    fig, ax = _plot_figure(X_TITLE, dates)

    for locale in locales:
        locale_df = _filter_locale(df, locale)
        for temp_type in ['Min', "Max"]:
            values = locale_df.select(pl.col(temp_type)).get_columns()[0].to_list()
            label = f"{locale}-{temp_type}"
            ax.plot(dates, values, label=label, marker=_to_marker(label))

    ax.set_title(TITLE)  # Add a title to the axes.
    ax.legend(bbox_to_anchor=(1.1, 1.05), fancybox=True, shadow=True)  # Add a legend.
    fig.savefig(file)
    return file


def _plot_figure(name, dates):
    fig, ax = plt.subplots(figsize=(15, 7), layout='constrained')
    # ax.set_xticks(range(0, len(dates)))
    # ax.set_xticklabels(dates)
    ax.set_xlabel(name)  # Add an x-label to the axes.
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))

    ax.set_ylabel(Y_TITLE)  # Add a y-label to the axes.

    ax.grid(True)
    return fig, ax


def _to_marker(locale):
    return markers[hash(locale) % 16]


def _unique_recorded_for(df):
    unique_dates = (df.unique(subset=['RecordedFor'])
                    .sort(pl.col('RecordedFor'))
                    .select(pl.col('RecordedFor')).rows())
    return [date[0] for date in unique_dates]


def _filter_locale_temp_type(df, locale, temp_type):
    return (df.filter(pl.col('Locale') == locale)
            .select(pl.col(temp_type)))


def _filter_locale(df, locale):
    return (df.filter(pl.col('Locale') == locale)
            .sort(pl.col('RecordedAt'))
            .select(pl.col('Min'), pl.col('Max')))


def _unique_locales(df):
    unique_locales = df.unique(subset=['Locale'], maintain_order=True).select(pl.col('Locale')).rows()
    return [locale[0] for locale in unique_locales]


# def _markers2():
#     star = mpath.Path.unit_regular_star(6)
#     circle = mpath.Path.unit_circle()
#     # concatenate the circle with an internal cutout of the star
#     cut_star = mpath.Path(
#         vertices=np.concatenate([circle.vertices, star.vertices[::-1, ...]]),
#         codes=np.concatenate([circle.codes, star.codes]))
#
#     return {'star': star, 'circle': circle, 'cut_star': cut_star}
