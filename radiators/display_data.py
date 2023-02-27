"""
Display radiator monitor logs

Figure is presented in a popup to the user if run directly, or returned
as a byte object for rendering as an img HTML source.
"""

from io import BytesIO
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


def display_data(timescale='24h', display=False):
    """Load temperature logs and return png image buffer for rendering.

    Arguments
        display:    display image to screen (default when run directly)
    """
    log_file_name = 'temperatures.csv'
    df = pd.read_csv(
            log_file_name,
            header=None,
            names=[
                'datetime',
                'device_name',
                'target_temp',
                'current_temp',
                'radiator_on',
                ]
            )
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    df = df.last(timescale)
    device_names = df['device_name'].unique()

    if display:
        fig, axs = plt.subplots(len(device_names), 1)
    else:
        fig = Figure(figsize=[8, 12])
        axs = fig.subplots(len(device_names), 1)
    ymax = 0.5+max(max(df['target_temp']), max(df['current_temp']))
    xmin = min(df.index)
    xmax = max(df.index)
    status_line = 1.0   # y-location of status line
    for device_ix, device_name in enumerate(device_names):
        ax = axs[device_ix]
        device_df = df[df['device_name'] == device_name]
        ax.plot(        # Temperature
                device_df.index,
                device_df['current_temp'],
                label="Temperature",
                zorder=1,
                )
        ax.plot(        # Target temperature
                device_df.index,
                device_df['target_temp'],
                label="Target",
                linewidth=1,
                zorder=0,
                color=(1, 0.5, 0.1),
                )
        ax.plot(        # Background line (indicates no log records)
                [xmin, xmax],
                [status_line, status_line],
                linewidth=1,
                color=(0.8, 0.8, 0.8),
                zorder=2,
                )
        cmap, norm = mcolors.from_levels_and_colors(
                [-0.2, 1, 2],
                ['green', 'red'])
        ax.scatter(     # Place marks when radiator is known to be ON or OFF
                device_df.index,
                status_line+np.zeros(len(device_df.index)),
                c=device_df['radiator_on'],
                cmap=cmap,
                norm=norm,
                marker='s',
                s=5,
                label="OFF/ON",
                zorder=3,
                )
        ax.set_ylabel(device_name)
        ax.set_ylim(0, ymax)
        ax.set_xlim(xmin, xmax)
        # pylint: disable=anomalous-backslash-in-string
        ax.text(0.8, 0.8, rf"{device_df['current_temp'][-1]}$^\circ$C",
                transform=ax.transAxes, color="black", fontsize=15)
        if device_ix == 0:
            ax.legend(loc='upper left')
    if display:
        plt.show()
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    return buf


if __name__ == "__main__":
    display_data(display=True)
