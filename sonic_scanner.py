import numpy as np
import wave
from scipy.fftpack import fft
from scipy.io.wavfile import read
from scipy import signal
import composition
import note

BUFFER_SIZE = 1024
SEGMENT_SIZE = 1024

def create_note(freq, seg_num, ampl):
    start_time = seg_num*SEGMENT_SIZE
    return note.Note(start_time = start_time, frequency = freq, amplitude=ampl)

# copy of main right now
def scan() :
    print("Freq detection")
    wave_ifile = wave.open('sound1.wav', 'r')
    frame_rate = wave_ifile.getframerate()
    hamming_window = signal.hamming(SEGMENT_SIZE)
    comp = composition.Composition()
    segment_num=0

    while True:
        iframes = wave_ifile.readframes(BUFFER_SIZE)
        if not iframes:
            break

        data = np.fromstring(iframes, np.int16)[0:SEGMENT_SIZE]
        fft_data = fft(data,SEGMENT_SIZE) *hamming_window
        bin_number = fft_data.argmax(axis=0)
        amplitude = fft_data[bin_number]
        freq = bin_number /SEGMENT_SIZE *frame_rate
        comp.add_note( create_note(freq, segment_num, amplitude) )
        segment_num+=1

    wave_ifile.close()

    return comp

if __name__ == "__main__" :
    print("Freq detection")
    wave_ifile = wave.open('sound1.wav', 'r')
    frame_rate = wave_ifile.getframerate()
    hamming_window = signal.hamming(SEGMENT_SIZE)
    comp = composition.Composition()
    segment_num=0

    while True:
        iframes = wave_ifile.readframes(BUFFER_SIZE)
        if not iframes:
            break

        data = np.fromstring(iframes, np.int16)[0:SEGMENT_SIZE]
        fft_data = fft(data,SEGMENT_SIZE) *hamming_window
        bin_number = fft_data.argmax(axis=0)
        amplitude = fft_data[bin_number]
        freq = bin_number /SEGMENT_SIZE *frame_rate
        comp.add_note( create_note(freq, segment_num, amplitude) )
        segment_num+=1

    wave_ifile.close()
