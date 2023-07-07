import numpy as np

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
