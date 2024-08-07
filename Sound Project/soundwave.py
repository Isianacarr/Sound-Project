#SoundWave.py
#<fixMe> needs comments


class SoundWave:

    def __init__(self,samples=[]):
        self._samples = list(samples)

    def __len__(self):
        returnlen(self._samples)

    def __getitem__(self, i):
        return self._samples[i]
