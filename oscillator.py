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


import matplotlib.pyplot as plt

# Generate a 1-second tone at 440 Hz
frequency = 440
duration = 1

# Create the oscillators
sineOsc = sine_oscillator()
squareOsc = square_oscillator()
triangleOsc = triangle_oscillator()
sawtoothOsc = sawtooth_oscillator()
noiseOsc = noise_oscillator()

# Generate the tones
sine_wave = sineOsc.tone(frequency, duration)
sine_wave_harmonics = sineOsc.tone(frequency, duration, harmonics=[0.5, 0.3, 0.2])
square_wave = squareOsc.tone(frequency, duration)
triangle_wave = triangleOsc.tone(frequency, duration)
sawtooth_wave = sawtoothOsc.tone(frequency, duration)
noise_wave = noiseOsc.tone(duration)

# Plot the waveforms
plt.figure(figsize=(15, 10))

plt.subplot(3, 2, 1)
plt.plot(sine_wave[:1000])
plt.title("Sine Wave")

plt.subplot(3, 2, 2)
plt.plot(sine_wave_harmonics[:1000])
plt.title("Sine Wave with Harmonics")

plt.subplot(3, 2, 3)
plt.plot(square_wave[:1000])
plt.title("Square Wave")

plt.subplot(3, 2, 4)
plt.plot(triangle_wave[:1000])
plt.title("Triangle Wave")

plt.subplot(3, 2, 5)
plt.plot(sawtooth_wave[:1000])
plt.title("Sawtooth Wave")

plt.subplot(3, 2, 6)
plt.plot(noise_wave[:1000])
plt.title("Noise Wave")

plt.tight_layout()
plt.show()
