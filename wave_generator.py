import numpy as np
from pylab import plot
from pylab import show
from scipy import signal
import composition
import wave
import math

def square_wave( length, amplitude, frequency ) :
    section = frequency // 2
    x = np.linspace(amplitude, amplitude, section)
    mx = -x

    t = np.concatenate( (x, mx) )
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

def noise_wave( length, amplitude ) :
    t = np.random.rand(length)
    t = np.multiply(t,amplitude)

    return t

def mix_waves( waves ):
    mix = np.zeros[len(waves[0])]
    for wave in waves :
        mix = np.add(mix,wave)
    return mix

def write_to_file( data, filename, params ):
    f = wave.open( filename,'w' )
    f.setparams( params )
    f.writeframes( data.astype(np.int16).tostring() )

def generate( composition ) :
    notes = composition.notes
    s_wave = np.array([])
    for note in notes :
        length = note.end_time - note.start_time
        s_wave = np.concatenate( (s_wave, square_wave(length, 10000, 1/(note.frequency/44100))) )
    params = (1, 2, 44100, len(n_wave), 'NONE', 'not compressed')
    write_to_file(s_wave, 'square.wav', params)



if __name__ == "__main__" :
    s_wave = np.array([])
    t_wave = np.array([])
    i = 100
    for i in range(100,4000,10):
        s_wave = np.concatenate( (s_wave, square_wave(44100/100, 10000, 1/(i/44100))) )
        t_wave = np.concatenate( (t_wave, triangle_wave(44100/100, 10000, 1/(i/44100))) )

    n_wave = noise_wave( 44100*10, 10000 )

    params = (1, 2, 44100, len(n_wave), 'NONE', 'not compressed')
    write_to_file(s_wave, 'square.wav', params)
    write_to_file(t_wave, 'triangle.wav', params)
    write_to_file(n_wave, 'noise.wav', params)
    '''plot(n_wave)
    show()
    print(len(n_wave))
    print("GENERATESOUND")'''
