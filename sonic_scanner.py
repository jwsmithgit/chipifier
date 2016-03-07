import numpy as np
import wave
from scipy.fftpack import fft,rfft
from scipy.io.wavfile import read
from scipy import signal
import composition
import note
import matplotlib.pyplot as ml
import cmath

BUFFER_SIZE = 1024
SEGMENT_SIZE = 1024

def create_note(freq, seg_num, ampl):
    start_time = seg_num * SEGMENT_SIZE
    end_time = start_time + SEGMENT_SIZE-1
    return note.Note(start_time, end_time, freq, ampl)

#COPIED REMOVE
def parabolic(f, x):
    """Quadratic interpolation for estimating the true position of an
    inter-sample maximum when nearby samples are known.

    f is a vector and x is an index for that vector.

    Returns (vx, vy), the coordinates of the vertex of a parabola that goes
    through point x and its two neighbors.

    Example:
    Defining a vector f with a local maximum at index 3 (= 6), find local
    maximum if points 2, 3, and 4 actually defined a parabola.

    In [3]: f = [2, 3, 1, 6, 4, 2, 3, 1]

    In [4]: parabolic(f, argmax(f))
    Out[4]: (3.2142857142857144, 6.1607142857142856)

    """
    xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)

# copy of main right now
def scan() :
    print("Freq detection")
    wave_ifile = wave.open('sound1.wav', 'r')
    frame_rate = wave_ifile.getframerate()
    comp = composition.Composition()
    segment_num=0

    while True:
        iframes = wave_ifile.readframes(BUFFER_SIZE)
        if not iframes:
            break

        data = np.fromstring(iframes, np.int16)
        windowed = data * signal.hamming(len(data))

        fft_data = fft(windowed)
        bin_number = np.argmax(abs(fft_data))
        #bin_number = parabolic(np.log(abs(fft_data)), bin_number)[0]

        complex_coordinate = fft_data[bin_number] /SEGMENT_SIZE*10
        amplitude = cmath.polar(complex_coordinate)[0]

        freq = bin_number /SEGMENT_SIZE *frame_rate
        comp.add_note( create_note(freq, segment_num, amplitude) )
        segment_num+=1

    wave_ifile.close()

    return comp

if __name__ == "__main__" :
    scan()
