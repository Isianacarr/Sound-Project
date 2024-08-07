# test_soundwave.py

import unittest
import os

from soundwave import SoundWave
from tonelibjz import generate_tone

INCLUDE_MANUAL_TESTS = False


class TestSoundWave(unittest.TestCase):

    def setUp(self):
        # this method automatically runs before each test
        #  so we always have a "fresh" copy of these objects

        self.samples1 = [.75, .25, 0.0, -.25, -.5]
        self.sw1 = SoundWave(self.samples1)

        self.samples2 = [-.75, -1.0, -.75]
        self.sw2 = SoundWave(self.samples2)

    def test_len(self):
        self.assertEqual(len(SoundWave()), 0)
        self.assertEqual(len(self.sw1), 5)
        self.assertEqual(len(self.sw2), 3)

    """

    def test_getitem(self):
        self.assertEqual(self.sw1[0], .75)
        self.assertEqual(self.sw1[2], 0.0)
        self.assertEqual(list(self.sw1), self.samples1)

    def test_extend(self):
        self.sw1.extend(self.sw2)
        self.assertEqual(list(self.sw1), self.samples1 + self.samples2)

    def test_duration(self):
        self.assertAlmostEqual(self.sw1.duration(), 1/44100*5)
        self.assertAlmostEqual(self.sw2.duration(), 1/44100*3)

    def test_maxamp(self):
        self.assertAlmostEqual(self.sw1.maxamp(), .75)
        self.assertAlmostEqual(self.sw2.maxamp(), 1.0)

    def test_clamp(self):
        sw = SoundWave([0.5, 1.5, 0.0, -.5, -2.3])
        sw.clamp()
        self.assertEqual(list(sw), [0.5, 1.0, 0.0, -.5, -1.0])

    def test_normalize(self):
        self.sw1.normalize()
        self.assertEqual(list(self.sw1), [1.0, 1/3, 0.0, -1/3, -2/3])

        self.sw2.normalize()
        self.assertEqual(list(self.sw2), self.samples2)

    def test_add(self):
        sw3 = self.sw1 + self.sw2
        self.assertEqual(list(sw3), [0.0, -0.75, -.75, -.25, -.5])

    def test_mul(self):
        sw3 = self.sw1 * 2
        self.assertEqual(list(sw3), [1.5, .5, 0., -.5, -1.])

    def test_rmul(self):
        sw3 = 2 * self.sw1
        self.assertEqual(list(sw3), [1.5, .5, 0., -.5, -1.])

    # Manual tests

    def test_play(self):
        if not INCLUDE_MANUAL_TESTS:
            return
        sw = SoundWave(generate_tone())
        sw.play()

    def test_tofile(self):
        if not INCLUDE_MANUAL_TESTS:
            return
        sw = SoundWave(generate_tone())
        os.remove("test_tone_file.wav")
        sw.tofile("test_tone_file.wav")
    
    """


if __name__ == "__main__":
    unittest.main()
