import numpy as np
import mido
from mido import MidiFile
import sounddevice as sd
from oscillator import *
from modulator import *
from mixer import *
from envelope import *
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

f = 880  # Frequency (e.g. A4)
duration = 0.25  # Duration in seconds (shorter for visualization)

# Frequencies for C4 major scale
# C4, D4, E4, F4, G4, A4, B4, C5
frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]


# Frequency ratios for the first several harmonics of a piano
# These are approximate and can be tweaked to your liking
harmonic_ratios = [1, 2, 3, 4, 5, 6, 7]

# Amplitude of each harmonic
# The amplitude generally decreases as the frequency increases
harmonic_amps = [1.0, 0.5, 0.33, 0.25, 0.2, 0.167, 0.14]

# Generate a tone with the harmonics
# Create oscillators
sineOsc = sine_oscillator()
squareOsc = square_oscillator()
triangleOsc = triangle_oscillator()
ampMod = amplitude_modulator()
freqMod = frequency_modulator()

tone = sineOsc.tone(f, duration, harmonic_amps)

# Define envelope parameters
a = 0.1  # Attack time (0-1)
d = 0.2  # Decay time in (0-1)
s = 0.4  # Sustain level (0-1)
r = 0.7  # Release time (0-1)

# Apply the envelope
adsr = envelope(a, d, s, r)

mixer = Mixer()

# Apply the envelope
adsr = envelope(a, d, s, r)


def play_midi_file(file_path):
    midi_file = MidiFile(file_path)

    tempo = 500000  # Default MIDI tempo (microseconds per beat)
    ticks_per_beat = midi_file.ticks_per_beat

    all_tones = []  # A list to store all tones
    for i, track in enumerate(midi_file.tracks):
        print("Track {}: {}".format(i, track.name))
        note_start_times = {}
        note_velocities = {}
        for msg in track:
            if msg.is_meta:
                print(msg)
                if msg.type == "set_tempo":
                    tempo = msg.tempo
                    msg.tempo = mido.bpm2tempo(216 * 3)
            else:
                if msg.type == "note_on":
                    # Store the start time of the note
                    note_start_times[msg.note] = msg.time
                    note_velocities[msg.note] = msg.velocity
                elif msg.type == "note_off":
                    # Calculate the duration of the note
                    note_duration_ticks = msg.time - note_start_times[msg.note]
                    note_duration_seconds = mido.tick2second(
                        note_duration_ticks, ticks_per_beat, tempo
                    )

                    # Convert MIDI note to frequency (this is an approximation)
                    frequency = 440.0 * (2.0 ** ((msg.note - 69) / 12.0))

                    # Generate tone with the frequency and velocity from the MIDI event
                    sintone = freqMod.modulate(
                        sineOsc.tone(frequency, note_duration_seconds),
                        frequency,
                        0.8,
                        note_duration_seconds,
                    )
                    squaretone = ampMod.modulate(
                        squareOsc.tone(frequency, note_duration_seconds),
                        frequency,
                        0.1,
                        note_duration_seconds,
                    )
                    triangletone = ampMod.modulate(
                        triangleOsc.tone(frequency, note_duration_seconds),
                        frequency,
                        0.5,
                        note_duration_seconds,
                    )
                    mixer.tracks.clear()
                    mixer.add_track(sintone, 0.6)
                    mixer.add_track(squaretone, 0.23)
                    mixer.add_track(triangletone, 0.12)
                    tone = mixer.mix()

                    # Modulate the tone with the ADSR envelope
                    tone = adsr.apply(tone)

                    mixer.tracks.clear

                    # Add the tone to the all_tones list
                    all_tones.extend(tone * note_velocities[msg.note])

    # Convert the list of tones to a numpy array
    output = np.array(all_tones)

    # Normalize the output to the range [-1, 1]
    output /= np.abs(output).max()

    # Finally, play the output
    output = np.int16(output * 32767)  # converting from float32 to int16
    write("output.wav", SAMPLE_RATE, output)
    sd.play(output, samplerate=SAMPLE_RATE, blocking=True)


play_midi_file("slip-jig-de-chocobo.mid")
