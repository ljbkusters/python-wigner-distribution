#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
smoothed_wigner_dist.py
@author Luc Kusters
@date 08-08-2022
"""
import numpy
from matplotlib import pyplot

import wignerdpy
from wignerdpy.toolkits import signal_toolkit


def smoothed_wd(signal, samples):
    """Get the smoothed wigner distribution"""
    wigner_dist, max_freq = wignerdpy.wigner_distribution(
            signal, sample_frequency=samples.sample_frequency)
    wd = wignerdpy.interference_reduced_wigner_distribution(
            wigner_dist)
    return wd


def plot_wd(wd, title):
    """Plot the wigner distribution"""
    fig, ax = pyplot.subplots()
    ax.imshow(wd, aspect="auto")
    ax.set_xlabel("time")
    ax.set_ylabel("frequency")
    ax.set_title(title)
    fig.savefig(title.lower().replace(" ", "_"))
    # pyplot.show()
    pyplot.close(fig)


if __name__ == "__main__":
    TIME_SAMPLES = signal_toolkit.DEFAULT_TIME_SAMPLES
    SINE_50HZ = signal_toolkit.sine_wave(TIME_SAMPLES.samples, frequency=50)
    SINE_100HZ = signal_toolkit.sine_wave(TIME_SAMPLES.samples, frequency=100)
    MIXED_SINES = SINE_50HZ + SINE_100HZ

    wd = smoothed_wd(MIXED_SINES, TIME_SAMPLES)
    plot_wd(wd, "Mixed sine smoothed wigner distribution")

    SAMPLES = signal_toolkit.TimeSamples.from_sample_number(2**6)
    CROSS_CHIRP = (signal_toolkit.chirp(SAMPLES, 1, 20)
                   + signal_toolkit.chirp(SAMPLES, 20, 1))
    wd = smoothed_wd(CROSS_CHIRP, SAMPLES)
    plot_wd(wd, "Cross chirp smoothed wigner distribution")
