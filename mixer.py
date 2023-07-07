import numpy as np


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
