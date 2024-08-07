# tonelib.py

"""Simple tone generation library for creating, playing, and saving audio tones.

A tone is represented as a list of "samples" of the waveform where
each sample is a floating point number in the range -1 to 1
inclusive. Sampling is done at the standard CD rate of 44100 hz.

The generate_tone function produces a list of samples representing
a tone of a given frequency, duration, and amplitude produced from
a standard wave function.

Filter functions modify a list of samples, for example, by making a 
tone "fade-out" or adjusting the overall volume.

write_wavefile writes a list of samples to an uncompressed wav file.

play_sound is a simple function for playing tones. Intended for
testing purposes only.

"""

import math
import wave
import struct
import subprocess
import random
import sys
import os

from wavefns import *

SAMPLERATE = 44100  # samples per second


def generate_tone(wavefn=sinewave, freq=440, duration=1, amp=1):
    """Create a tone with given characteristics.

    params: wavefn is a standard wave function (see wavefns.py),
            frequency is in hz, duration is in seconds, amplitude is a
            float in range 0..1.

    returns a list of floats representing sequential samples of
              a tone with the given waveform, frequency, duration,
              and amplitude.
    """
    n = SAMPLERATE * duration
    t = 0
    samples = []

    for i in range(n):
        sample = amp * wavefn(math.tau * freq * t)
        samples.append(sample)
        t += 1/SAMPLERATE

    return samples

def volumefilter(samples, factor=.75):
    """ Adjust the amplitude of entire sample uniformly.

    pre: factor > 0
    post: Every sample in samples has been multiplied by factor.

    note: factor > 1.0 amplifies while factor < 1.0 decreases volume.
    """
    for i in range(len(samples)):
        sample * factor

def decayfilter(samples, decaytime=.5, SAMPLERATE=44100):
    """ Exponential taper of tone amplitude.

    pre: decaytime > 0

    post: Values in samples have been decreased with increasing
          damping from the begining to end. The rate of damping is
          determined by decaytime, which is the half-life of the
          amplitude.  So the sample at decaytime is reduced by .5, the
          sample at 2*decaytime is reduced by .25, etc.
    """
    factor = .5 ** (1/SAMPLERATE * decaytime)

    for i in range(len(samples)):
        samples [ i ] *= factor ** i
    
                    

######################################################################
# The below functions are done


def write_wavefile(samples, fname, SAMPLERATE=44100):
    """ Write sampled wave to a wav format sound file

    pre: samples is a list representing a valid sound sample.
    post: The sound information has been written to the file fname in
          wav audio file format.

    Note: This function wipes out any previous contents of file, fname.
    """

    wfile = wave.open(fname, 'w')
    nframes = len(samples)
    wfile.setparams((1, 4, SAMPLERATE, nframes, 'NONE', 'not compressed'))
    for b in _bytestream(samples):
        wfile.writeframesraw(b)
    wfile.close()


def _bytestream(samples):
    max_amplitude = 2.0**31 - 1.0
    for sample in samples:
        sample = max(-1, min(sample, 1))   # clamp to -1..1
        value = int(max_amplitude*sample)
        binary = struct.pack('i', value)
        yield binary


# playing sounds varies by platform. play_sound is set to the
# appropriate function so that calling play_sound(tone_samples) should
# work on most machines.

# WARNING: on Windows and MacOs play_sound creates (and then DELETES)
#          a file called "temp.wav"

def _play_sound_linux(samples):
    """Play sound on Linux system

    pre: samples is a list representing a valid sound sample.
    post: The sound has been piped to an external process for playback.

    Note: This should work on any Linux system using ALSA.
    """
    pipes = subprocess.Popen(["aplay",
                              "-fS32_LE",
                              "-c1",
                              "-r{:d}".format(SAMPLERATE),
                              "-q",
                              "-"],
                             stdin=subprocess.PIPE)
    wfile = pipes.stdin
    for binary in _bytestream(samples):
        wfile.write(binary)
    wfile.close()


def _play_sound_mac(samples):
    """ play sound on a mac

        This is a bit of a hack: write to a temp file and call
        the MacOs command to play the file.
    """
    write_wavefile(samples, "temp.wav")
    subprocess.call(["afplay", "temp.wav"])
    os.remove("temp.wav")


def _play_sound_windows(samples):
    write_wavefile(samples, "temp.wav")
    winsound.PlaySound("temp.wav",
                       winsound.SND_FILENAME & winsound.SND_ASYNC)
    os.remove("temp.wav")


# define play_sound to be the platform appropriate function

if sys.platform == "win32":
    import winsound
    play_sound = _play_sound_windows
elif sys.platform == "linux":
    play_sound = _play_sound_linux
elif sys.platform == "darwin":
    play_sound = _play_sound_mac


def test():
    while True:
        freq = int(input("frequency: "))
        if freq == 0:
            break
        play_sound(generate_tone(freq=freq))


if __name__ == "__main__":
    test()
