import numpy as np
from scipy import signal
from oscillator import *

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
    def modulate(self, waveform, frequency, depth, duration):
        # Generate time array
        t = np.arange(int(SAMPLE_RATE * duration)) / SAMPLE_RATE

        # Generate modulation signal
        modulator_signal = depth * np.sin(2 * np.pi * frequency * t)

        # Generate PWM wave
        pwm_wave = signal.square(2 * np.pi * frequency * t + modulator_signal)

        return pwm_wave


import matplotlib.pyplot as plt

# Generate a 1-second tone at 440 Hz
frequency = 440
depth = 0.5
modulation_frequency = 5
duration = 1

# Create the oscillators and modulators
sineOsc = sine_oscillator()
freqMod = frequency_modulator()
ampMod = amplitude_modulator()
ringMod = ring_modulator()
pwmMod = pulse_width_modulator()
squareOsc = square_oscillator()

# Generate the tones
sine_wave = sineOsc.tone(frequency, duration)
freq_modulated_wave = freqMod.modulate(sine_wave, modulation_frequency, depth, duration)
amp_modulated_wave = ampMod.modulate(sine_wave, modulation_frequency, depth, duration)
ring_modulated_wave = ringMod.modulate(sine_wave, modulation_frequency, depth, duration)
square_wave = squareOsc.tone(frequency, duration)
pwm_modulated_wave = pwmMod.modulate(sine_wave, modulation_frequency, depth, duration)


# Plot the waveforms
plt.figure(figsize=(15, 10))

plt.subplot(3, 2, 1)
plt.plot(sine_wave[:1000])
plt.title("Original Sine Wave")

plt.subplot(3, 2, 2)
plt.plot(freq_modulated_wave[:1000])
plt.title("Frequency Modulated Wave")

plt.subplot(3, 2, 3)
plt.plot(amp_modulated_wave[:1000])
plt.title("Amplitude Modulated Wave")

plt.subplot(3, 2, 4)
plt.plot(ring_modulated_wave[:1000])
plt.title("Ring Modulated Wave")

plt.subplot(3, 2, 5)
plt.plot(square_wave[:1000])
plt.title("Original Square Wave")

plt.subplot(3, 2, 6)
plt.plot(pwm_modulated_wave[:1000])
plt.title("Pulse Width Modulated Wave")

plt.tight_layout()
plt.show()
