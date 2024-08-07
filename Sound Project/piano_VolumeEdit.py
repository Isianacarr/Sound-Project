# piano_VolumeEdit.py
#    Interactive testing program for the tonelib. Play a scale with the
#      a-k keys. Uppercase for next octave up.
#Isiana, Feyi, Shaukat, Michael, Carlos

from __future__ import division, print_function

from graphics import *
from tonelibjz import *


class Button:

    """A button is a labeled rectangle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it."""

    def __init__(self, win, center, width, height, label):
        """ Creates a rectangular button, eg:
        qb = Button(myWin, centerPoint, width, height, 'Quit') """

        w, h = width/2.0, height/2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        "Returns true if button active and p is inside"
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)

    def getLabel(self):
        "Returns the label string of this button."
        return self.label.getText()

    def activate(self):
        "Sets this button to 'active'."
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = True

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = False


class Piano:

    def __init__(self):
        self.win = GraphWin("CS 220 Piano", 400, 200)
        self.win.setCoords(0, 0, 100, 100)
        self.wavefn = sinewave
        self.amplitude = 1

        bspecs = [(10, "Sine"), (30, "Triangle"), (50, "Square"),
                  (70, "Sawtooth"), (90, "Noise")]
        self.buttons = [Button(self.win, Point(x, 25), 18, 10, label)
                        for x, label in bspecs]
        for b in self.buttons[1:]:
            b.activate()

        self.duration = .5
        self.durationText = Text(Point(25, 75), "Duration: 0.5")
        self.durationText.draw(self.win)
        self.durationDown = Button(self.win, Point(20, 60), 5, 10, "v")
        self.durationDown.activate()
        self.durationUp = Button(self.win, Point(30, 60), 5, 10, "^")
        self.durationUp.activate()

        self.decay = .25
        self.decayText = Text(Point(75, 75), "Decay: 0.25")
        self.decayText.draw(self.win)
        self.decayDown = Button(self.win, Point(70, 60), 5, 10, "v")
        self.decayDown.activate()
        self.decayUp = Button(self.win, Point(80, 60), 5, 10, "^")
        self.decayUp.activate()

        self.volume = .5
        self.volumeText = Text(Point(50, 75), "Volume: 0.5")
        self.volumeText.draw(self.win)
        self.volumeDown = Button(self.win, Point(45, 60), 5, 10, "v")
        self.volumeDown.activate()
        self.volumeUp = Button(self.win, Point(55, 60), 5, 10, "^")
        self.volumeUp.activate()

    def changeDuration(self, amt):
        self.duration += amt
        self.duration = max(self.duration, 0.1)
        self.durationText.setText("Duration: "+str(round(self.duration, 1)))

    def changeDecay(self, amt):
        self.decay += amt
        self.decay = max(self.decay, 0.05)
        self.decayText.setText("Decay: {:0.2f}".format(self.decay))

    def changeVolume(self, amt):
        self.volume += amt
        self.volume = max(self.volume, 0.05)
        self.volumeText.setText("Volume: {:0.2f}".format(self.volume))

    def play(self):
        k = self.win.checkKey()
        while k.lower() != "q":
            self.handleMouseClick()
            freq = self.getFreq(k)
            if freq > 0:
                sound = generate_tone(wavefn=self.wavefn,
                                      amp=self.amplitude,
                                      freq=freq, duration=self.duration)
                decayfilter(sound, self.decay)
                volumefilter(sound, self.volume)
                play_sound(sound)
            k = self.win.checkKey()
        self.win.close()

    def handleMouseClick(self):
        pt = self.win.checkMouse()
        if pt is not None:
            if self.decayUp.clicked(pt):
                self.changeDecay(0.05)
            elif self.decayDown.clicked(pt):
                self.changeDecay(-0.05)
            elif self.durationUp.clicked(pt):
                self.changeDuration(0.1)
            elif self.durationDown.clicked(pt):
                self.changeDuration(-0.1)
            elif self.volumeUp.clicked(pt):
                self.changeVolume(0.5)
            elif self.volumeDown.clicked(pt):
                self.changeVolume(-0.5)
            else:
                self.checkWaveButtons(pt)

    def checkWaveButtons(self, pt):
        for b in self.buttons:
            if b.clicked(pt):
                chosen = b.getLabel()
                self.setWave(chosen)
                for b in self.buttons:
                    if b.getLabel() == chosen:
                        b.deactivate()
                    else:
                        b.activate()

    def setWave(self, s):
        if s == "Sine":
            self.wavefn = sinewave
            self.amplitude = 1
        elif s == "Triangle":
            self.wavefn = trianglewave
            self.amplitude = 1
        elif s == "Square":
            self.wavefn = squarewave
            self.amplitude = .4
        elif s == "Sawtooth":
            self.wavefn = sawtoothwave
            self.amplitude = .5
        elif s == "Noise":
            self.wavefn = whitenoise
            self.amplitude = .5

    def getFreq(self, key):
        letter = key.lower()
        if letter == "a":
            f = 261.6256
        elif letter == "s":
            f = 293.6648
        elif letter == "d":
            f = 329.6276
        elif letter == "f":
            f = 349.2282
        elif letter == "g":
            f = 391.9954
        elif letter == "h":
            f = 440.0
        elif letter == "j":
            f = 493.8833
        elif letter == "k":
            f = 523.2511
        else:
            f = 0.0

        # Shift key used for next ocatve
        if key.isupper():
            f = 2 * f

        return f


if __name__ == "__main__":
    try:
        app = Piano()
        app.play()
    except GraphicsError as e:
        # Avoid error messages from "xing out" the grpahics window
        # ignore closed window errors, re-raise anythin else
        if "closed window" not in str(e):
            raise e
