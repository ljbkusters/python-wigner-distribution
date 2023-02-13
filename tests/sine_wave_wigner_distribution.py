#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_wvd.py
@author Luc Kusters
@date 17-03-2022
"""

import numpy
from matplotlib import pyplot

import wignerdpy
from wignerdpy.toolkits import signal_toolkit


def plot_wigner_distribution(
        wigner_distribution, title, min_time=0, max_time=1,
        min_freq=0, max_freq=1, xlabel="Time (s)",
        ylabel="Frequency (Hz)", save=True,
        ):
    # plot figure
    fig, ax = pyplot.subplots()
    ax.imshow(numpy.abs(wigner_distribution),
              extent=(min_time, max_time, min_freq, max_freq),
              aspect="auto")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if save:
        fig.savefig(title.lower().replace(" ", "_"))
    return fig, ax


TIME_SAMPLES = signal_toolkit.DEFAULT_TIME_SAMPLES

SINE_50HZ = signal_toolkit.sine_wave(TIME_SAMPLES.samples, frequency=50)
SINE_100HZ = signal_toolkit.sine_wave(TIME_SAMPLES.samples, frequency=100)
MIXED_SINES = SINE_50HZ + SINE_100HZ

for (signal, title) in (
            (SINE_50HZ, "Wigner Distribution Sine Wave 50Hz"),
            (SINE_100HZ, "Wigner Distribution Sine Wave 100Hz"),
            (MIXED_SINES, "Wigner Distribution Mixed Sine 50Hz + 100Hz")
            ):
    wigner_dist, max_freq = wignerdpy.wigner_distribution(
            signal, sample_frequency=TIME_SAMPLES.sample_frequency)
    plot_wigner_distribution(wigner_dist, title, max_freq=max_freq,
                             min_time=TIME_SAMPLES.t0,
                             max_time=TIME_SAMPLES.t1)

