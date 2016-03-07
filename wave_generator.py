import numpy as np
import composition

def generate_sinusoid( t, frequency, amplitude, phase ):
	sinusoid = amplitude * sin( 2*pi * frequency * t + phase )
	return sinusoid

def square_wave( length, amplitude, frequency ) :
	t = np.linspace(0, length, frequency, endpoint=False)
	t = signal.square(2 * np.pi * t))
	return t

def triangle_wave( length, amplitude ):
	section = length // 4
	x = np.linspace(0, amplitude, section+1)
	mx = -x
	return np.r_[x, x[-2::-1], mx[1:], mx[-2:0:-1]]

if __name__ == "__main__" :
	t_wave = triangle_wave(100,5)
	s_wave = square_wave(100,5,440)
	print(len(t_wave))
	print("GENERATESOUND")
