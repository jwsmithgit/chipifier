import wave
import math
import cmath

import numpy as np
import scipy as sp
#from scipy.fftpack import fft,rfft
#from scipy import signal

import composition
import note

import sys
sys.path.append('./peakutils/')
import peak as pk

BUFFER_SIZE = 1024
SEGMENT_SIZE = 1024

'''def create_note( freq, seg_num, ampl ):
    start_time = seg_num * SEGMENT_SIZE
    end_time = start_time + SEGMENT_SIZE-1
    return note.Note( start_time, end_time, freq, ampl )
'''

# create FFT estimation
def fft_frequency( data, fs ) :
    windowed = data * sp.signal.hamming( len(data) )

    fft_data = sp.fftpack.fft( windowed )

    bin_i = np.argmax( abs(fft_data) )
    frequency = bin_i * ( fs / len(fft_data) )

    return frequency

def fft_amplitude( data ) :
    fft_data = sp.fftpack.fft( data ) / len(data)

    amplitude = 0
    for i in range(len(fft_data)//2) :
        # the amplitude is the radius retrieved form real number and imaginary number
        complex_coordinate = abs(fft_data[i]) #np.amax( abs(fft_data) )
        amplitude += cmath.polar( complex_coordinate )[0]

    return amplitude

# create autocorrelation estimation
def autocorrelation_frequency( data, fs ) :
    # check for silence
    if not np.any( data ) :
        return 0

    mean = np.mean( data )
    data = np.subtract( data, mean )

    # time lag multiplyer
    corr = sp.signal.fftconvolve( data, data[::-1] )
    # only want the end of the data, where it tapers
    corr = corr[-len(data):]

    # want bin number of first positive number
    variance = np.diff(corr)
    start = np.where(variance > 0)[0][0]
    bin_i = np.argmax( corr[start:] ) + start

    # sampling rate / bin number(peak)
    frequency = fs / bin_i

    return frequency
    
# create overlapping windows from wav file
def get_file_overlap( filename ) :
    print( "creating overlapping wav frames..." )
    
    wave_ifile = wave.open( filename, 'r' )
    frame_rate = wave_ifile.getframerate()
    frames = []
    frame_size = 1024
    hop_size = 128

    frame = []
    while True:
        iframes = wave_ifile.readframes( frame_size - len(frame) )
        if not iframes:
            break

        data = np.fromstring( iframes, np.int16 )

        frame.extend( data )
        frames.append( frame )

        frame = frame[hop_size:]

    wave_ifile.close()

    frames[-1].extend([0] * (frame_size - len(frames[-1])))
    return frames
    
def get_frequency_spectrum( frames ) :
    print( "creating frequency spectrum..." )

    windowed = frames * sp.signal.hamming( len(frames[0]) )
    frequency_spectrum = sp.fftpack.fft( windowed )

    return frequency_spectrum
    
def get_magnitude_spectrum( frequency_spectrum ) :
    print( "creating magnitude spectrum..." )

    magnitude_spectrum = np.absolute( frequency_spectrum )

    return magnitude_spectrum
 
def get_log_power_spectrum( magnitude_spectrum ) :
    print( "creating log power magnitude spectrum..." )

    log_power_spectrum = np.log( 1 + 1000.0 * magnitude_spectrum )

    return log_power_spectrum
    
def get_flux( magnitude_spectrum, log_power_spectrum ) :
    print( "creating flux..." )

    magnitude_difference = magnitude_spectrum[1:] - np.roll(magnitude_spectrum,1,axis=0)[1:]
    indicator = np.where( magnitude_difference <= 0, 0, 1 )

    flux_parts = (log_power_spectrum[1:] - np.roll(log_power_spectrum,1,axis=0)[1:]) * indicator
    flux_frames = np.sum( flux_parts, axis=1 )

    return flux_frames
    
def apply_low_pass_filter( frames ) :
    print( "applying low pass filter..." )

    low_pass = sp.signal.firwin( 15, 7, nyq=344.5/2 )
    low_passed = sp.signal.lfilter( low_pass, 1.0, frames )

    return low_passed
    
def get_oss_overlap( oss ) :
    print( "creating overlapping oss frames..." )
    
    frames = []
    frame_size = 2048
    hop_size = 128

    frame = []
    while True:
        iframes = oss[: frame_size - len(frame) ]
        oss = oss[ len(iframes) :]
        if len(oss) == 0 :
            break

        frame.extend( iframes )
        frames.append( frame )

        frame = frame[hop_size:]

    frames[-1].extend([0] * (frame_size - len(frames[-1])))
    return np.array( frames )
    
def generalized_autocorrelation( frames ) :
    print( "creating autocorrelation frames..." )
    
    padded_frames = np.lib.pad( frames, ( (0,0), (0, len(frames[0])) ), 'constant', constant_values=(0, 0) )
    frequency_spectrum = sp.fftpack.fft( padded_frames )
    magnitude_spectrum = np.absolute( frequency_spectrum )
    powered = np.power( magnitude_spectrum, 0.5 )
    auto_frames = np.real( sp.fftpack.ifft( powered ) )
    auto_frames = auto_frames[:, :len(frames[0])]
    
    return auto_frames
    
def enhance_harmonics( a1 ) :
    print( "creating enhanced harmonics..." )
    a2 = np.repeat( autocorrelated, 2, axis=1 )
    a4 = np.repeat( autocorrelated, 4, axis=1 )
    
    a2 = a2[:, :len(a1[0])]
    a4 = a4[:, :len(a1[0])]
    
    enhanced = a1 + a2 + a4
    
    return enhanced
   
def peak_tempo( frames ) :
    print( "picking peaks..." )

    max_peaks = 137+np.argmax( frames[:,137:414], axis=1 )
    peak_counts = np.bincount( max_peaks )
    lag = np.argmax(peak_counts)
    tempo = 60*344.5/lag
    
    return tempo
    
def get_oss( filename ) :
    
    overlap = get_file_overlap( filename )
    frequency_spectrum = get_frequency_spectrum( overlap )
    magnitude_spectrum = get_magnitude_spectrum( frequency_spectrum )
    log_power_spectrum = get_log_power_spectrum( magnitude_spectrum )
    flux_frames = get_flux( magnitude_spectrum, log_power_spectrum )
    oss = apply_low_pass_filter(flux_frames)
    
    return oss
    
def get_tempo( oss ) :
    
    oss_overlap = get_oss_overlap( oss )
    autocorrelated = generalized_autocorrelation( oss_overlap )
    enhanced = enhance_harmonics( autocorrelated )
    tempo = peak_tempo( enhanced )
    tempo = int( round( tempo ) )
    
    return tempo

def beat_scan( filename ) :
    print( "Beat/Note onset detection" )
    
    #oss = get_oss( filename )
    oss = get_oss( 'hardsnes.wav' )
    peaks = pk.indexes( oss ) 
    beats = peaks * 44100/344.5
    beats = list(map(int, beats))
    
    return beats
    
    """wave_ifile = wave.open( filename, 'r' )
    frame_rate = wave_ifile.getframerate()
    comp = composition.Composition()
    segment_num = 0

    while True:
        iframes = wave_ifile.readframes( BUFFER_SIZE )
        if not iframes:
            break

        data = np.fromstring( iframes, np.int16 )
        comp.add_raw_window_average(abs(sum(data)/len(data)))
        #frequency = autocorrelation_frequency( data, frame_rate )
        #amplitude = fft_amplitude( data )

        #comp.add_note( create_note( frequency, segment_num, amplitude ) )
        segment_num += 1

    wave_ifile.close()

    return comp"""

def note_scan( filename, beats ) :
    print( "Freq detection" )
    wave_ifile = wave.open( filename, 'r' )
    frame_rate = wave_ifile.getframerate()
    
    compo = composition.Composition()
    
    for i,beat in enumerate(beats) :
        if i == 0 :
            note_length = beats[i]
        else :
            note_length = beats[i] - beats[i-1]
        
        iframes = wave_ifile.readframes( note_length )
        if not iframes:
            break

        
        data = np.fromstring( iframes, np.int16 )

        frequency = autocorrelation_frequency( data, frame_rate )
        amplitude = fft_amplitude( data )

        compo.add_note( , frequency, amplitude  )
        compo.add_note( frequency, segment_num, amplitude )
        note.set_frequency( frequency )
        note.set_amplitude( amplitude )

    wave_ifile.close()

    return composition
    
    '''for note in composition.beat_notes :
        note_length = note.end_time - note.start_time
        iframes = wave_ifile.readframes( note_length )
        if not iframes:
            break

        data = np.fromstring( iframes, np.int16 )

        frequency = autocorrelation_frequency( data, frame_rate )
        amplitude = fft_amplitude( data )

        note.set_frequency( frequency )
        note.set_amplitude( amplitude )
   '''

if __name__ == "__main__" :
    scan( 'sound1.wav' )
