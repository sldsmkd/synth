import numpy as np
from scipy.fft import fft, ifft


class NullFilter:
    def apply(self, signal):
        return signal


class LowPassFilter(NullFilter):
    def __init__(self, cutoff, sample_rate):
        self.cutoff = cutoff
        self.sample_rate = sample_rate

    def apply(self, signal):
        # Perform an FFT on the signal
        spectrum = fft(signal)

        # Create an array of frequencies
        frequencies = np.linspace(0, self.sample_rate, len(spectrum))

        # Create the filter
        filter_array = frequencies < self.cutoff

        # Apply the filter to the spectrum
        filtered_spectrum = spectrum * filter_array

        # Perform an inverse FFT to get the time-domain signal
        filtered_signal = ifft(filtered_spectrum).real

        return filtered_signal


class HighPassFilter(NullFilter):
    def __init__(self, cutoff, sample_rate):
        self.cutoff = cutoff
        self.sample_rate = sample_rate

    def apply(self, signal):
        spectrum = fft(signal)
        frequencies = np.linspace(0, self.sample_rate, len(spectrum))
        filter_array = frequencies > self.cutoff
        filtered_spectrum = spectrum * filter_array
        filtered_signal = ifft(filtered_spectrum).real

        return filtered_signal


class BandPassFilter(NullFilter):
    def __init__(self, low_cutoff, high_cutoff, sample_rate):
        self.low_cutoff = low_cutoff
        self.high_cutoff = high_cutoff
        self.sample_rate = sample_rate

    def apply(self, signal):
        spectrum = fft(signal)
        frequencies = np.linspace(0, self.sample_rate, len(spectrum))
        filter_array = (frequencies > self.low_cutoff) & (
            frequencies < self.high_cutoff
        )
        filtered_spectrum = spectrum * filter_array
        filtered_signal = ifft(filtered_spectrum).real

        return filtered_signal


class NotchFilter(NullFilter):
    def __init__(self, low_cutoff, high_cutoff, sample_rate):
        self.low_cutoff = low_cutoff
        self.high_cutoff = high_cutoff
        self.sample_rate = sample_rate

    def apply(self, signal):
        spectrum = fft(signal)
        frequencies = np.linspace(0, self.sample_rate, len(spectrum))
        filter_array = (frequencies < self.low_cutoff) | (
            frequencies > self.high_cutoff
        )
        filtered_spectrum = spectrum * filter_array
        filtered_signal = ifft(filtered_spectrum).real

        return filtered_signal
