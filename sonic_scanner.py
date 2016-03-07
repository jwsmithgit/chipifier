import numpy as np
import scipy as sp
import wave
from scipy.fftpack import fft
from scipy.io.wavfile import read

BUFFER_SIZE = 1024
WINDOW_SIZE = 1024

if __name__ == "__main__" :
    print("Freq detection")
    wave_ifile = wave.open('sound1.wav', 'r')
    print( wave_ifile.getparams() )
    frame_rate = wave_ifile.getframerate()
    print(frame_rate)
    print(WINDOW_SIZE)

    while True:
        iframes = wave_ifile.readframes(BUFFER_SIZE)
        if not iframes:
            break

        data = np.fromstring(iframes, np.int16)[0:WINDOW_SIZE]
        fft_data = fft(data,WINDOW_SIZE)
        freq = fft_data.argmax(axis=0) /WINDOW_SIZE *frame_rate
        print(freq)


    wave_ifile.close()
    




