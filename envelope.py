import numpy as np
from modulator import amplitude_modulator, frequency_modulator
from oscillator import sine_oscillator, square_oscillator, triangle_oscillator

SAMPLE_RATE = 44100


class envelope:
    def __init__(self, a, d, s, r):
        self.a = a
        self.d = d
        self.s = s
        self.r = r

    def apply(self, signal):
        total_length = len(signal)

        a_length = int(self.a * total_length)
        d_length = int(self.d * total_length)
        s_length = int(self.s * total_length)
        r_length = int(self.r * total_length)

        # If the sum of ADSR lengths is larger than total_length, recalculate sustain length
        if a_length + d_length + s_length + r_length > total_length:
            s_length = total_length - a_length - d_length - r_length

        a_section = np.linspace(0, 1, a_length)
        d_section = np.linspace(1, self.s, d_length)
        s_section = np.ones(s_length) * self.s
        r_section = np.linspace(self.s, 0, r_length)

        envelope = np.concatenate([a_section, d_section, s_section, r_section])

        # Make envelope and signal the same length
        if len(envelope) < total_length:
            envelope = np.concatenate(
                [envelope, np.zeros(total_length - len(envelope))]
            )

        return signal * envelope


import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# Define our oscillator
osc = sine_oscillator()
duration = 1.0  # 1 second duration
frequency = 440.0  # 440 Hz (standard A note)

# Generate the tone
tone = osc.tone(frequency, duration)

# Define some different envelopes
env1 = envelope(
    0.1, 0.1, 0.6, 0.2
)  # fast attack, short decay, long sustain, fast release
env2 = envelope(
    0.2, 0.2, 0.2, 0.4
)  # slow attack, slow decay, short sustain, long release
env3 = envelope(
    0.01, 0.01, 0.98, 0.0
)  # very fast attack, very short decay, very long sustain, no release

# Apply the envelopes to the tone
tone_env1 = env1.apply(tone)
tone_env2 = env2.apply(tone)
tone_env3 = env3.apply(tone)

# Plot the results
plt.figure(figsize=(12, 8))

plt.subplot(311)
plt.title("Envelope 1")
plt.plot(tone_env1)
plt.ylim(-1.5, 1.5)

plt.subplot(312)
plt.title("Envelope 2")
plt.plot(tone_env2)
plt.ylim(-1.5, 1.5)

plt.subplot(313)
plt.title("Envelope 3")
plt.plot(tone_env3)
plt.ylim(-1.5, 1.5)

plt.tight_layout()
plt.show()
