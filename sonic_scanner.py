import wave
import math
import cmath

import numpy as np
from scipy.fftpack import fft,rfft
from scipy.io.wavfile import read
from scipy import signal

import composition
import note

BUFFER_SIZE = 1024
SEGMENT_SIZE = 1024

def create_note( freq, seg_num, ampl ):
    start_time = seg_num * SEGMENT_SIZE
    end_time = start_time + SEGMENT_SIZE-1
    return note.Note( start_time, end_time, freq, ampl )

# create FFT estimation
def fft_frequency( data, fs ) :
    windowed = data * signal.hamming( len(data) )

    fft_data = fft( windowed )

    bin_i = np.argmax( abs(fft_data) )
    frequency = bin_i * ( fs / len(fft_data) )

    return frequency

def fft_amplitude( data ) :
    fft_data = fft( data ) / len(data)

    amplitude = 0
    for i in range(len(fft_data)//2) :
        # the amplitude is the radius retrieved form real number and imaginary number
        complex_coordinate = abs(fft_data[i]) #np.amax( abs(fft_data) )
        amplitude += cmath.polar( complex_coordinate )[0]

    return amplitude

# create overlapping windows estimation

# create autocorrelation estimation
def autocorrelation_frequency( data, fs ) :
    mean = np.mean( data )
    data = np.subtract( data, mean )

    # time lag multiplyer
    corr = signal.fftconvolve( data, data[::-1] )
    # only want the end of the data, where it tapers
    corr = corr[-len(data):]

    # want bin number of first positive number
    variance = np.diff(corr)
    start = np.where(variance > 0)[0][0]
    bin_i = np.argmax( corr[start:] ) + start

    # sampling rate / bin number(peak)
    frequency = fs / bin_i

    return frequency

def scan( filename ) :
    print( "Freq detection" )
    wave_ifile = wave.open( filename, 'r' )
    frame_rate = wave_ifile.getframerate()
    comp = composition.Composition()
    segment_num = 0

    while True:
        iframes = wave_ifile.readframes( BUFFER_SIZE )
        if not iframes:
            break

        data = np.fromstring( iframes, np.int16 )
        frequency = autocorrelation_frequency( data, frame_rate )
        amplitude = fft_amplitude( data )

        comp.add_note( create_note( frequency, segment_num, amplitude ) )
        segment_num += 1

    wave_ifile.close()

    return comp

if __name__ == "__main__" :
    scan( 'sound1.wav' )
