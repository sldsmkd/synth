class Delay:
    def __init__(self, delay_time, feedback, mix, sample_rate=44100):
        self.delay_samples = int(delay_time * sample_rate)
        self.feedback = feedback
        self.mix = mix
        self.buffer = np.zeros(self.delay_samples)
        self.pos = 0

    def process(self, signal):
        output = np.zeros_like(signal)
        for i, s in enumerate(signal):
            delayed_sample = self.buffer[self.pos]
            output[i] = s + delayed_sample * self.mix
            self.buffer[self.pos] = s + delayed_sample * self.feedback
            self.pos = (self.pos + 1) % self.delay_samples
        return output
