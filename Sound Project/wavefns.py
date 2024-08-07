# wavefns.py
"""Simple periodic waveform functions.

 A "standard" wave function (such as sin) is a periodic function with
 period equal to 2*pi (also known as tau) and a amplitude of 1.
"""
import math
import random
pi = math.pi


def sinewave(t):
    """ Standard periodic sine wave generator
    pre: t >= 0
    post returns value of standard sine wave at time t
         (0 at t=0, 1 at t= pi/2, 0 at pi, -1 at 1.5*pi, 0 at 2*pi)
    """

    return math.sin(t)


def squarewave(t):
    """ Standard periodic square wave generator.

    pre: t >= 0
    post: returns value of standard square wave at time t.
          (1.0 for 0 <= t < pi and -1.0 for pi <= t < 2*pi)
    """
    if 0 <= t% (2*math.pi) < math.pi:
        return 1
    elif math.pi <= t % (2*math.pi )< 2*math.pi:
        return -1

def trianglewave(t):
    """ Standard periodic triangle wave generator.

    pre: t >= 0
    post: returns value of standard triangle wave at time t.
          (0.0 at t=0, 1.0 at t=pi/2, 0.0 at t=pi, -1.0 at t=1.5*pi)
    """
    if 0<= t % math.tau < math.pi / 2:
        return (( 2 / pi ) * t) - 4*(t // math.tau)
    elif math.pi / 2 < t % math.tau < (3*pi)/2:
        return (( -2 / pi ) * t + 2) + 4*(t // math.tau)
    elif (3*pi)/2 < t % math.tau < math.tau:
        return (( 2 / pi ) * t - 4) - 4*(t // math.tau)

def sawtoothwave(t):
    """ Standard periodic sawtooth wave generator.

    pre: t >= 0
    post: returns value of standard sawtooth wave at time t.
          (0.0 at t=0, rising to 1 near t=pi, -1.0 at t=pi, rising to 0.0 at t=pi)
    """
    if 0<= t % math.tau < math.pi:
        return (( 1 / pi ) * t) - 2*(t // math.tau)
    elif math.pi < t % math.tau < math.tau:
        return (( 1 / pi ) * t - 2) - 2*(t // math.tau)
        


def whitenoise(t):
    """ White noise "wave" generator

    post: returns random float value in range -1 to 1
    """
    return random.random() * 2 - 1
    
    
######################################################################
# The rest of this is for testing purposes. No changes needed.
# Requires: graphics needed to visualize the wave forms

def _plot(wavefn):
    # test function plots 2 cycles of wavefunction
    win = GraphWin(wavefn.__name__, 600, 200)
    win.setCoords(0, -1, 2*math.tau, 1)
    Line(Point(0, 0), Point(2*math.tau, 0)).draw(win)
    npoints = 300
    dt = 2*math.tau/npoints
    t = 0
    last = Point(t, wavefn(t))
    for i in range(npoints):
        t += dt
        p = Point(t, wavefn(t))
        segment = Line(last, p).draw(win)
        segment.setFill("red")
        segment.setWidth(2)
        last = p
    win.getMouse()
    win.close()


if __name__ == "__main__":
    from graphics import *
    for wf in [sinewave, squarewave, trianglewave, sawtoothwave, whitenoise]:
        _plot(wf)
