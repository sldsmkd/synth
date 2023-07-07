import numpy as np
from scipy import signal

SAMPLE_RATE = 44100


class oscillator:
    def tone(self, duration):
        t = np.arange(int(SAMPLE_RATE * duration)) / SAMPLE_RATE
        return t


class sine_oscillator(oscillator):
    def tone(self, frequency, duration, harmonics=[]):
        t = np.arange(int(SAMPLE_RATE * duration)) / SAMPLE_RATE
        wave = np.sin(2 * np.pi * frequency * t)
        for i, h in enumerate(harmonics, start=1):
            wave += h * np.sin(2 * np.pi * (i + 1) * frequency * t)
        return wave


class square_oscillator(oscillator):
    def tone(self, frequency, duration):
        t = np.arange(int(SAMPLE_RATE * duration)) / SAMPLE_RATE
        return 0.5 * signal.square(2 * np.pi * frequency * t)


class triangle_oscillator(oscillator):
    def tone(self, frequency, duration):
        t = np.arange(int(SAMPLE_RATE * duration)) / SAMPLE_RATE
        return 0.5 * signal.sawtooth(2 * np.pi * frequency * t, 0.5)


class sawtooth_oscillator(oscillator):
    def tone(self, frequency, duration):
        t = np.arange(int(SAMPLE_RATE * duration)) / SAMPLE_RATE
        return 0.5 * signal.sawtooth(2 * np.pi * frequency * t)


class noise_oscillator(oscillator):
    def tone(self, duration):
        return np.random.normal(0, 0.5, int(SAMPLE_RATE * duration))
