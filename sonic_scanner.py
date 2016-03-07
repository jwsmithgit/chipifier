import wave
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

def scan() :
    print( "Freq detection" )
    wave_ifile = wave.open( 'sound1.wav', 'r' )
    frame_rate = wave_ifile.getframerate()
    comp = composition.Composition()
    segment_num = 0

    while True:
        iframes = wave_ifile.readframes( BUFFER_SIZE )
        if not iframes:
            break

        data = np.fromstring( iframes, np.int16 )
        windowed = data * signal.hamming( len(data) )

        fft_data = fft( windowed )
        bin_number = np.argmax( abs(fft_data) )

        freq = bin_number * ( frame_rate / SEGMENT_SIZE ) 
	# need to crush to musical notes
	# A0 is 27.5 all steps are multiplied by 12root(2) or 1.0594 steps up until A9 14080
	# see monophonic pitch slide 24

	# the amplitude is the radius retrieved form real number and imaginary number
        complex_coordinate = fft_data[bin_number] # * ( 10 / SEGMENT_SIZE )
        amplitude = cmath.polar( complex_coordinate )[0]

        comp.add_note( create_note( freq, segment_num, amplitude ) )
        segment_num += 1

    wave_ifile.close()

    return comp

if __name__ == "__main__" :
    scan()
