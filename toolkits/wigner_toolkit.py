#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wigner_toolkit.py
@author Luc Kusters
@date 17-03-2022
"""

import numpy
from scipy import signal, linalg, ndimage


def wigner_distribution(x, use_analytic=True, sample_frequency=None,
                        t_0=0, t_1=1, flip_frequency_range=True):
    """Discrete Pseudo Wigner Ville Distribution based on [1]

    Args:
        x, array like, signal input array of length N
        use_analytic, bool, whether or not to use analytic associate of input
            data x by default set to True
        sample_frequency, sampling frequency
        t_0, time at which the first sample was recorded
        t_1, time at which the last sample was recorded
        flip_frequency_range, flip the data in about the time axis such that
            the minimum frequency is in the left bottom corner.

    Returns:
        wigner_distribution, N x N matrix
        frequency_bins, array like, length N frequency range

    References:
        [1] T. Claasen & W. Mecklenbraeuker, The Wigner Distribution -- A Tool
        For Time-Frequency Signal Analysis, Phillips J. Res. 35, 276-300, 1980
    """

    # Ensure the input array is a numpy array
    if not isinstance(x, numpy.ndarray):
        x = numpy.asarray(x)
    # Compute the autocorrelation function matrix
    if x.ndim != 1:
        raise ValueError("Input data should be one dimensional time series.")
    # Use analytic associate if set to True
    if use_analytic:
        if all(numpy.isreal(x)):
            x = signal.hilbert(x)
        else:
            raise RuntimeError("Keyword 'use_analytic' set to True but signal"
                               " is of complex data type, but analytic signals"
                               " must be real valued")

    # calculate the wigner distribution
    N = x.shape[0]
    bins = numpy.arange(N)
    indices = linalg.hankel(bins, bins + N - (N % 2))

    padded_x = numpy.pad(x, (N, N), 'constant')
    wigner_integrand = \
        padded_x[indices+N] * numpy.conjugate(padded_x[indices[::, ::-1]])

    wigner_distribution = numpy.real(numpy.fft.fft(wigner_integrand, axis=1)).T

    # calculate sample frequency
    if sample_frequency is None:
        sample_frequency = N / (t_1 - t_0)

    # calculate frequency range
    if use_analytic:
        max_frequency = sample_frequency/2
    else:
        max_frequency = sample_frequency/4

    # flip the frequency range
    if flip_frequency_range:
        wigner_distribution = wigner_distribution[::-1, ::]

    return wigner_distribution, max_frequency


def interference_reduced_wigner_distribution(
        wigner_distribution, number_smoothing_steps=16,
        t_filt_max_percentage=0.03, f_filt_max_percentage=0.02):
    """Method for reducing interference terms based on [1]

    Params:
        wigner_distribution, array like, N x N discrete wigner distribution
        matrix

    Returns:
        interference reduced wigner distribution, N x N ndarray

    Uses a method for interference reduction based on Pikula et al. [1].
    The method works by executing multiple smoothings using a gaussian
    filter, in this implementation using the scipy.ndimage module. The
    optimal smoothing per time-frequency bin is then chosen. Pikula et al.
    [1] goes into more detail on how this optimal smoothing can be chosen.

    The output is then a distribution which contains mainly autoterms with
    strongly suppressed interference terms, better representing the actual
    signal that is present. This, however, destroys many of the
    distributions' mathematical properties, and should only serve as an
    analysis tool for autoterms.

    References:
        [1] Pikula, Stanislav & Beneš, Petr. (2020). A New Method for
        Interference Reduction in the Smoothed Pseudo Wigner-Ville
        Distribution. International Journal on Smart Sensing and
        Intelligent Systems. 7. 1-5. 10.21307/ijssis-2019-101.
    """
    # Ensure the input array is a numpy array
    if not isinstance(wigner_distribution, numpy.ndarray):
        wigner_distribution = numpy.asarray(wigner_distribution)
    # Compute the autocorrelation function matrix
    if wigner_distribution.ndim != 2:
        raise ValueError("Input data should be a two dimensional discrete"
                         " wigner distribution.")
    N_f, N_t = wigner_distribution.shape
    t_filter_widths = \
        numpy.linspace(0, N_t * t_filt_max_percentage, number_smoothing_steps)
    f_filter_widths = \
        numpy.linspace(0, N_f * f_filt_max_percentage, number_smoothing_steps)

    # filter at various filtration widths
    smoothed_wigner_distributions = \
        numpy.zeros((number_smoothing_steps, N_f, N_t))
    for i, (f_fw, t_fw) in enumerate(zip(t_filter_widths, f_filter_widths)):
        smoothed_wigner_distributions[i] = \
            ndimage.gaussian_filter(wigner_distribution, sigma=(f_fw, t_fw))

    # differential analysis per time-frequency bin
    first_derivative = numpy.diff(smoothed_wigner_distributions, axis=0)
    smoothing_index_best_guess = numpy.argmax(numpy.abs(first_derivative),
                                              axis=0)

    # choose smoothing per time-frequency bin
    x, y, z = smoothed_wigner_distributions.shape
    interference_reduced_wigner_distribution = \
        smoothed_wigner_distributions[
                smoothing_index_best_guess,
                numpy.arange(y)[::, numpy.newaxis],
                numpy.arange(z)[numpy.newaxis, ::]]
    return interference_reduced_wigner_distribution
