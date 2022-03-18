#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_wvd.py
@author Luc Kusters 
@date 17-03-2022 
@mail <ljbkusters@gmail.com>
"""

import numpy
from matplotlib import pyplot
from toolkits import wigner_toolkit


def plot_wigner_distribution(wigner_distribution, title, min_time=0, max_time=1, 
                             min_freq=0, max_freq=1, xlabel="Time (s)", 
                             ylabel="Frequency (Hz)", save=True):
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

def signal_sine_wave(signal_frequency, sample_frequency, time_min=0, time_max=1):
    time_delta = time_max - time_min
    sample_number = int(sample_frequency / time_delta)
    time_samples = numpy.linspace(time_min, time_max, sample_number)
    signal = numpy.sin(time_samples*2*numpy.pi*signal_frequency)
    return signal, time_samples

SAMPLE_FREQ = 1e3
SINE_50HZ, _ = signal_sine_wave(signal_frequency=50, sample_frequency=SAMPLE_FREQ)
SINE_100HZ, _ = signal_sine_wave(signal_frequency=100, sample_frequency=SAMPLE_FREQ)
MIXED_SINES = SINE_50HZ + SINE_100HZ

for (signal, title) in (
            (SINE_50HZ, "Wigner Distribution Sine Wave 50Hz"), 
            (SINE_100HZ, "Wigner Distribution Sine Wave 100Hz"),
            (MIXED_SINES, "Wigner Distribution Mixed Sine 50Hz + 100Hz")
            ):
    wigner_dist, max_freq = wigner_toolkit.wigner_distribution(signal)
    plot_wigner_distribution(wigner_dist, title, max_freq=max_freq)
