#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wigner_toolkit.py
@author Luc Kusters 
@date 17-03-2022 
"""

import numpy
import scipy
from scipy import signal, linalg

def wigner_distribution(x, use_analytic=True, sample_freq=None, t_0=0, t_1=1, 
                        flip_frequency_range=True):
    """Discrete Pseudo Wigner Ville Distribution based on [1]

    Args:
        x, array like, signal input array of length N
        use_analytic, bool, whether or not to use analytic associate of input data x
            by default set to True
        sample_freq, sampling frequency
        t_0, time at which the first sample was recorded
        t_1, time at which the last sample was recorded
        flip_frequency_range, flip the data in about the time axis such that the minimum
                              frequency is in the left bottom corner.

    Returns:
        wigner_distribution, N x N matrix
        frequency_bins, array like, length N frequency range

    References:
        [1] T. Claasen & W. Mecklenbraeuker, The Wigner Distribution -- A Tool For 
        Time-Frequency Signal Analysis, Phillips J. Res. 35, 276-300, 1980
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
            raise RuntimeError("Keyword 'use_analytic' set to True but signal is of"
                               " complex data type, but analytic signals must be real"
                               " valued")

    # calculate the wigner distribution
    N = x.shape[0]
    bins = numpy.arange(N)
    indices = linalg.hankel(bins, bins + N - N%2)

    padded_x = numpy.pad(x, (N, N), 'constant')
    wigner_integrand = padded_x[indices+N]*numpy.conjugate(padded_x[indices[::, ::-1]])

    wigner_distribution = numpy.real(numpy.fft.fft(wigner_integrand, axis=1)).T
    
    # calculate sample frequency
    if sample_freq is None:
        sample_freq = N / (t_1 - t_0)

    # calculate frequency range
    if use_analytic:
        max_frequency = sample_freq/2
    else:
        max_frequency = sample_freq/4

    # flip the frequency range
    if flip_frequency_range:
        wigner_distribution = wigner_distribution[::-1, ::]

    return wigner_distribution, max_frequency
