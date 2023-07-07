import numpy as np
from scipy import signal

SAMPLE_RATE = 44100


class modulator:
    def modulate(self, waveform, frequency, depth, duration):
        return waveform


class frequency_modulator(modulator):
    def modulate(self, waveform, frequency, depth, duration):
        # Create the modulation signal
        t = np.arange(int(SAMPLE_RATE * duration)) / SAMPLE_RATE
        modulator_signal = depth * np.sin(2 * np.pi * frequency * t)

        # Generate a new carrier signal with modulated frequency
        carrier_frequency = (SAMPLE_RATE / len(waveform)) + modulator_signal
        return np.sin(2 * np.pi * carrier_frequency * t)


class amplitude_modulator(modulator):
    def modulate(self, waveform, frequency, depth, duration):
        # Create the modulation signal
        t = np.arange(int(SAMPLE_RATE * duration)) / SAMPLE_RATE
        modulator_signal = 1 + depth * np.sin(2 * np.pi * frequency * t)
        # Apply the modulation
        return waveform * modulator_signal


class ring_modulator(modulator):
    def modulate(self, waveform, frequency, depth, duration):
        # Create the modulation signal
        t = np.arange(int(SAMPLE_RATE * duration)) / SAMPLE_RATE
        modulator_signal = depth * np.sin(2 * np.pi * frequency * t)
        # Apply the modulation
        return waveform * modulator_signal


class pulse_width_modulator(modulator):
    ### broken
    def modulate(self, waveform, SAMPLE_RATE, frequency, depth, duration):
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
        modulator_signal = 0.5 + depth * np.sin(2 * np.pi * frequency * t)
        modulated_waveform = np.zeros_like(t)
        for i in range(len(t)):
            duty_cycle = modulator_signal[i]
            modulated_waveform[i] = (
                1 if (t[i] % (1 / frequency)) < duty_cycle / frequency else -1
            )
        return modulated_waveform
