import numpy as np
from pylab import plot
from pylab import show
from scipy import signal
import composition
import wave
import math
import random

def pulse_wave( length, amplitude, period, duty_cycles = 0.5 ) :
    section = period // ( 1 / duty_cycles )
    x = np.linspace(amplitude, amplitude, section)
    mx = -x

    for i in range( (int)( 1 / duty_cycles ) - 1 ) :
        x = np.concatenate( (x, mx) )

    t = x
    while len(t) < length :
        t = np.concatenate( (t, t) )
    t = t[:length]

    return t

def triangle_wave( length, amplitude, period ) :
    amplitude = amplitude * 4
    section = period // 4
    x = np.linspace(0, amplitude, section+1)
    mx = -x

    t = np.concatenate( (x, x[-2:0:-1], mx[1:], mx[-2:0:-1]) )
    while len(t) < length :
        t = np.concatenate( (t, t) )
    t = t[:length]

    return t
    
def noise_amplitude( amp, length ) :
    noise = np.linspace(amp, 0, 44100/4)
    if( len(noise) > length ) :
        noise = noise[:length]
        return noise
        
    silence = np.linspace(0, 0, length - len(noise))
    amp = np.r_[noise,silence]
    return amp

def noise_wave( length, amplitude, period, mode = 1 ) :
    t = [ ]

    #print( length )
    #period = 762
    #print( period )
    
    while len(t) < length :
        rcycle = random.randrange( math.floor(period) )
        x = np.linspace( amplitude, amplitude, rcycle )
        nx = np.linspace( -amplitude, -amplitude, period - rcycle )
        t = np.concatenate( (t, x, nx) )
    t = t[:length]
    
    '''
    if mode == 1 :
        t = np.random.choice( [0, amplitude], length )
    elif mode == 2 :
        t = np.random.choice( [0, amplitude], 93 )
        while len(t) < length :
            t = np.concatenate( (t, t) )
    '''

    if period > 200 :
        drum_amp = noise_amplitude( 0.4, len(t) )
    elif period > 50 :
        drum_amp = noise_amplitude( 0.8, len(t) )
    else :
        drum_amp = noise_amplitude( 0.2, len(t) )
    t = t*drum_amp

    return t

def mix_waves( waves ):
    print("mixing waves...")
    max_wave = 0
    for wave in waves :
        if len(wave) > max_wave :
            max_wave = len(wave)
            
    mix = np.zeros(max_wave)
    for wave in waves :
        level_wave = [x / len(waves) for x in wave]
        mix[:len(wave)] += level_wave
    return mix

def write_to_file( data, filename, params ):
    print("writing to file...")
    f = wave.open( filename,'w' )
    f.setparams( params )
    f.writeframes( data.astype(np.int16).tostring() )

def generate( composition ) :
    print("generating wave...")
    
    notes = composition.get_notes()
    channel = composition.get_channel()
    wave = [] #np.array([])
    for note in notes :
        length = note.get_end_time() - note.get_start_time()
        period = 1/(note.get_frequency()/44100)
        
        if note.get_frequency() < 1 :
            wave.extend( [0 for i in range(length)] )
        else :
            if channel == 1 or channel == 2 :
                wave.extend( pulse_wave(length, note.get_amplitude(), period, note.get_pwm()) )
            elif channel == 3 :
                wave.extend( triangle_wave(length, note.get_amplitude(), period) )
            elif channel == 4 :
                wave.extend( noise_wave(length, note.get_amplitude(), period) )
        '''
        if note.frequency < 1 :
            wave = np.concatenate( (wave, np.zeros(length)) )
        else :
            if channel == 1 or channel == 2 :
                wave = np.concatenate( (wave, pulse_wave(length, note.get_amplitude(), period, note.get_pwm()) ) )
            elif channel == 3 :
                wave = np.concatenate( (wave, triangle_wave(length, note.get_amplitude(), period) ) )
            elif channel == 4 :
                wave = np.concatenate( (wave, noise_wave(length, note.get_amplitude(), period) ) )
        '''

    return wave

if __name__ == "__main__" :
    s_wave = np.array([])
    t_wave = np.array([])

    for i in range(100,4000,10):
        s_wave = np.concatenate( (s_wave, pulse_wave(44100/100, 10000, 1/(i/44100))) )
        t_wave = np.concatenate( (t_wave, triangle_wave(44100/100, 10000, 1/(i/44100))) )

    s_wave = pulse_wave(44100*5, 10000, 1/(440/44100))
    t_wave = triangle_wave(44100*5, 10000, 1/(440/44100))
    frequency = 2093
    n_wave = noise_wave( 44100, 10000, 1/(frequency/44100) )

    params = (1, 2, 44100, len(n_wave), 'NONE', 'not compressed')
    write_to_file(s_wave, 'square.wav', params)
    write_to_file(t_wave, 'triangle.wav', params)
    write_to_file(n_wave, 'noise.wav', params)
