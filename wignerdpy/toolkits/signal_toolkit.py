#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
signal_toolkit.py
@author Luc Kusters
@date 23-03-2022
"""

import collections
import numpy
import scipy.signal


__SampleBase = collections.namedtuple(
            "__SampleBase",
            ("samples", "number_of_samples", "sample_frequency", "t0", "t1")
        )


class TimeSamples(__SampleBase):
    """Generalized time samples data structure

    Contains the samples in the form of a numpy.ndarray, the number of samples,
    the sample frequency, the start time, and the end time.

    Also contains factory methods for defining the time samples based on sample
    rate or number of samples.
    """

    @classmethod
    def from_sample_frequency(cls, sample_frequency, t0=0., t1=1.):
        time_delta = t1 - t0
        number_of_samples = int(float(sample_frequency) / float(time_delta))
        time_samples = numpy.linspace(t0, t1, number_of_samples)
        return cls(time_samples, number_of_samples, sample_frequency, t0, t1)

    @classmethod
    def from_sample_number(cls, number_of_samples, t0=0.1, t1=1.):
        time_delta = t1 - t0
        sample_frequency = float(float(number_of_samples) / float(time_delta))
        time_samples = numpy.linspace(t0, t1, number_of_samples)
        return cls(time_samples, number_of_samples, sample_frequency, t0, t1)


# signal sampled at 1024 Hz for a duration of 1 s
DEFAULT_TIME_SAMPLES = TimeSamples.from_sample_frequency(sample_frequency=1024)


def sine_wave(time_samples, frequency) -> numpy.ndarray:
    """Wrapper for numpy.sin to generate pure sine"""
    omega = 2 * numpy.pi * frequency
    return numpy.sin(time_samples * omega)


def chirp(time_samples, start_frequency,
          end_frequency, time_end=None) -> numpy.ndarray:
    """Wrapper for scipy.signal.chirp to generate linear chirps"""
    if time_end is None:
        time_end = numpy.max(time_samples.samples)
    return scipy.signal.chirp(time_samples.samples, f0=start_frequency,
                              t1=time_end, f1=end_frequency)


def gaussian(x, mean, std, height=1., bias=0.) -> numpy.ndarray:
    """Gaussian function

    Parameters:
        x, array like, input space
        mean, mean of gaussian
        std, standard deviation of gaussian
        heigt, max height of gaussian (relative to bias), by default 1.
        bias, bias of gaussian, by default 0.
    """
    exponential = numpy.exp(-0.5 * numpy.power((x - mean) / std, 2))
    return height * exponential + bias


def gaussian_kernel_sine(time_samples, frequency, envelope_mean, envelope_std)\
        -> numpy.ndarray:
    """Guassian windowed sine

    Produces a guassian kernel in the time-frequency domain of a
    Wigner distribution.
    """
    sine = sine_wave(time_samples, frequency)
    envelope = gaussian(time_samples, envelope_mean, envelope_std)
    return sine * envelope
