import numpy as np
from modulator import amplitude_modulator, frequency_modulator
from oscillator import sine_oscillator, square_oscillator, triangle_oscillator
import matplotlib.pyplot as plt

SAMPLE_RATE = 44100


class Mixer:
    def __init__(self):
        self.tracks = []

    def add_track(self, signal, weight=1.0):
        self.tracks.append((signal, weight))

    def mix(self):
        # Find the length of the longest track
        max_length = max(len(track[0]) for track in self.tracks)

        output = np.zeros(max_length)
        for signal, weight in self.tracks:
            # Pad the signal with zeros if it's shorter than the longest track
            if len(signal) < max_length:
                signal = np.pad(signal, (0, max_length - len(signal)))

            output += weight * signal

        # Normalize the output to the range [-1, 1]
        output /= np.abs(output).max()

        return output


# lets also graph a combo of sine, square and triangle passed through amp + freq mosulators and then mixed

# Create instances of oscillator and modulator
sine_osc = sine_oscillator()
square_osc = square_oscillator()
triangle_osc = triangle_oscillator()

amp_mod = amplitude_modulator()
freq_mod = frequency_modulator()

# Generate waveforms
sine_wave = sine_osc.tone(440, 1.0)  # 440 Hz sine wave for 1 second
square_wave = square_osc.tone(440, 1.0)
triangle_wave = triangle_osc.tone(440, 1.0)

# Apply amplitude modulation
sine_wave_amp_modulated = amp_mod.modulate(sine_wave, 5, 0.5, 1.0)
square_wave_amp_modulated = amp_mod.modulate(square_wave, 5, 0.5, 1.0)
triangle_wave_amp_modulated = amp_mod.modulate(triangle_wave, 5, 0.5, 1.0)

# Apply frequency modulation
sine_wave_freq_modulated = freq_mod.modulate(sine_wave, 5, 0.5, 1.0)
square_wave_freq_modulated = freq_mod.modulate(square_wave, 5, 0.5, 1.0)
triangle_wave_freq_modulated = freq_mod.modulate(triangle_wave, 5, 0.5, 1.0)

# Add to mixer
mixer_amp = Mixer()
mixer_amp.add_track(sine_wave_amp_modulated, 0.33)
mixer_amp.add_track(square_wave_amp_modulated, 0.33)
mixer_amp.add_track(triangle_wave_amp_modulated, 0.33)

mixer_freq = Mixer()
mixer_freq.add_track(sine_wave_freq_modulated, 0.33)
mixer_freq.add_track(square_wave_freq_modulated, 0.33)
mixer_freq.add_track(triangle_wave_freq_modulated, 0.33)

# Get the mixed output
output_amp = mixer_amp.mix()
output_freq = mixer_freq.mix()

# Plot the mixed waveforms
time = np.arange(0, 1.0, 1.0 / SAMPLE_RATE)  # Time array
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(time[:5000], output_amp[:5000])
plt.title("Amplitude Modulated Mixed Output")

plt.subplot(2, 1, 2)
plt.plot(time[:5000], output_freq[:5000])
plt.title("Frequency Modulated Mixed Output")

plt.tight_layout()
plt.show()
