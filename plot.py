import numpy as np
import sounddevice as sd
from oscillator import *
import matplotlib.pyplot as plt


def plot_waveform(waveform, sample_rate):
    t = np.arange(len(waveform)) / sample_rate
    plt.figure(figsize=(10, 4))
    plt.plot(t, waveform, label="Waveform")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title("Waveform")
    plt.legend()
    plt.show()


# Define some parameters
fs = 44100  # Sample rate
f = 440  # Frequency (e.g. A4)
duration = 0.02  # Duration in seconds (shorter for visualization)

# Generate and plot sine waveform
sineOsc = sine_oscillator()
sine_wave = sineOsc.tone(fs, f, duration)
plot_waveform(sine_wave, fs)

# Generate and plot square waveform
squareOsc = square_oscillator()
square_wave = squareOsc.tone(fs, f, duration)
plot_waveform(square_wave, fs)

# Generate and plot triangle waveform
triangleOsc = triangle_oscillator()
triangle_wave = triangleOsc.tone(fs, f, duration)
plot_waveform(triangle_wave, fs)

# Generate and plot sawtooth waveform
sawtoothOsc = sawtooth_oscillator()
sawtooth_wave = sawtoothOsc.tone(fs, f, duration)
plot_waveform(sawtooth_wave, fs)
