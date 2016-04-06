import numpy as np
from pylab import plot
from pylab import show
from scipy import signal
import composition
import wave
import math
import random

def pulse_wave( length, amplitude, frequency, duty_cycles = 0.25 ) :
    section = frequency // ( 1 / duty_cycles )
    x = np.linspace(amplitude, amplitude, section)
    mx = -x

    for i in range( (int)( 1 / duty_cycles ) - 1 ) :
        x = np.concatenate( (x, mx) )

    t = x
    while len(t) < length :
        t = np.concatenate( (t, t) )
    t = t[:length]

    return t

def triangle_wave( length, amplitude, frequency ) :
    section = frequency // 4
    x = np.linspace(0, amplitude, section+1)
    mx = -x

    t = np.concatenate( (x, x[-2:0:-1], mx[1:], mx[-2:0:-1]) )
    while len(t) < length :
        t = np.concatenate( (t, t) )
    t = t[:length]

    return t

def noise_wave( length, amplitude, frequency, mode = 1 ) :
    t = [ ]

    frequency = 762

    while len(t) < length :
        rcycle = random.randrange( math.floor(frequency) )
        x = np.linspace( amplitude, amplitude, rcycle )
        nx = np.linspace( -amplitude, -amplitude, frequency - rcycle )
        t = np.concatenate( (t, x, nx) )

    '''if mode == 1 :
        t = np.random.choice( [0, amplitude], length )
    elif mode == 2 :
        t = np.random.choice( [0, amplitude], 93 )
        while len(t) < length :
            t = np.concatenate( (t, t) )'''

    return t

def mix_waves( waves ):
    mix = np.zeros(len(waves[0]))
    for wave in waves :
        mix = np.add(mix,wave)
    return mix

def write_to_file( data, filename, params ):
    f = wave.open( filename,'w' )
    f.setparams( params )
    f.writeframes( data.astype(np.int16).tostring() )

def generate( composition, style="pulse" ) :
    notes = composition.notes
    wave = np.array([])
    for note in notes :
        length = note.end_time - note.start_time
        if note.frequency < 1 :
            wave = np.concatenate( (wave, np.zeros(length)) )
        else :
            if style == "pulse" :
                wave = np.concatenate( (wave, pulse_wave(length, note.amplitude, 1/(note.frequency/44100))) )
            elif style == "triangle" :
                wave = np.concatenate( (wave, triangle_wave(length, note.amplitude, 1/(note.frequency/44100))) )
            elif style == "noise" :
                wave = np.concatenate( (wave, noise_wave(length, note.amplitude, 1/(note.frequency/44100))) )

    params = (1, 2, 44100, len(wave), 'NONE', 'not compressed')
    write_to_file(wave, 'chiptune.wav', params)

if __name__ == "__main__" :
    s_wave = np.array([])
    t_wave = np.array([])

    for i in range(100,4000,10):
        s_wave = np.concatenate( (s_wave, pulse_wave(44100/100, 10000, 1/(i/44100))) )
        t_wave = np.concatenate( (t_wave, triangle_wave(44100/100, 10000, 1/(i/44100))) )

    s_wave = pulse_wave(44100*5, 10000, 1/(440/44100))
    t_wave = triangle_wave(44100*5, 10000, 1/(440/44100))
    n_wave = noise_wave( 44100*5, 10000, 1/(440/44100) )

    params = (1, 2, 44100, len(n_wave), 'NONE', 'not compressed')
    write_to_file(s_wave, 'square.wav', params)
    write_to_file(t_wave, 'triangle.wav', params)
    write_to_file(n_wave, 'noise.wav', params)
    '''plot(n_wave)
    show()
    print(len(n_wave))
    print("GENERATESOUND")'''
