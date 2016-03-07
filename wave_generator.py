import numpy as np
from pylab import plot
from pylab import show
from scipy import signal
import composition
import wave

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
		mix = [x + y for x, y in zip( mix, wave )]

	return mix

def write_to_file( data, filename, params ):
	f = wave.open( filename,'w' )
	f.setparams( params )
	f.writeframes( data.astype(np.int16).tostring() )

if __name__ == "__main__" :
	s_wave = square_wave(880,1,440)
	t_wave = triangle_wave(800,1,440)
	n_wave = noise_wave( 800, 1 )

	'''plot(n_wave)
	show()
	print(len(n_wave))
	print("GENERATESOUND")'''

	comp = composition.Composition()
