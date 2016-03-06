#import mir_eval
from pylab import *
import wave, struct

if __name__ == "__main__" :
    print("TRANSCRIBER")

    #s = mir_eval.io.load_wav("s.wav",False)
    #print(s)

    '''wave_ifile = wave.open('s.wav', 'r')

    nchannels = wave_ifile.getnchannels()
    sampwidth = wave_ifile.getsampwidth()

    BUFFER_SIZE = 2048

    nframes = BUFFER_SIZE / (nchannels*sampwidth)
    nframes = int(nframes)
    print(nframes)

    while True :
        iframes = wave_ifile.readframes(nframes)
        if not iframes :
            break

    wave_ifile.close()'''
