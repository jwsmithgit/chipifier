import math

# western music scale
# A0 is 27.5 all steps are multiplied by 12root(2) or 1.0594 steps up until A9 14080
# see csc475 monophonic pitch slide 24
def western_scale( ) :
    scale = [ 27.5 ]
    while scale[-1] <= 14080 :
        scale.append( scale[0] * ( math.pow( 2, len(scale) / 12 ) ) )

    return scale

def nes_pulse_scale( ) :
    cpu = 1789773
    scale = [ ]
    for i in range( 2048, 8, -1 ) :
        scale.append( cpu / ( 16 * ( i + 1 ) ) )
    return scale

def nes_triangle_scale( ) :
    cpu = 1789773
    scale = [ ]
    for i in range( 2048, 999, -1 ) :
        scale.append( cpu / ( 32 * ( i + 1 ) ) )
    return scale

# TODO nes noise scale
def nes_noise_scale( ) :
    cpu = 1789773
    scale = [ ]
    for i in range( 4068, 4, -1 ) :
        scale.append( cpu / ( 16 * i ) ) - 1
    # TODO not correct
    scale = 1/(scale/44100)
    return scale

class Scale :
    def __init__( self, scale ) :
        self.scale = [ ]

        if scale == "western" :
            self.scale = western_scale()

        elif scale == "pulse" :
            self.scale = nes_pulse_scale()

        elif scale == "triangle" :
            self.scale = nes_triangle_scale()

        elif scale == "noise" :
            self.scale = nes_noise_scale()
