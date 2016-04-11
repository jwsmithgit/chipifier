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

def nes_noise_scale( ) :
    cpu = 1789773
    scale = [ ]
    for i in range( 4068, 4, -1 ) :
        scale.append( cpu / ( 16 * i ) ) - 1
    # TODO not correct
    scale = 1/(scale/44100)
    return scale

def get_channel_scale( channel ) :
    if( channel == 1 or channel == 2 ) :
        return nes_pulse_scale( )
    elif( channel == 3 ) :
        return nes_triangle_scale( )
    elif( channel == 4 ) :
        return nes_noise_scale( )