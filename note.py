'''
NOTE class
a note is a sound that is made for a duration of time at a certain frequency
'''

class Note :
    # CONSTRUCTOR
    def __init__( self, start_time=-1, end_time=-1, frequency=-1, amplitude=-1, pwm=0.5 ) :
        self.start_time = start_time
        self.end_time = end_time
        self.frequency = frequency
        self.amplitude = amplitude
        self.pwm = pwm
        self.kick_note = False

    # SETTERS
    def set_start_time( self, start_time ) :
        self.start_time = start_time

    def set_end_time( self, end_time ) :
        self.end_time = end_time

    def set_frequency( self, frequency ) :
        self.frequency = frequency

    def set_amplitude( self, amplitude ) :
        self.amplitude = amplitude

    def set_pwm(self, pwm):
        self.pwm = pwm

    def set_kick(self, val):
        self.kick_note = val


    # GETTERS
    def get_start_time( self ) :
        return self.start_time

    def get_end_time( self ) :
        return self.end_time

    def get_frequency( self ) :
        return self.frequency

    def get_amplitude( self ) :
        return self.amplitude

    def get_pwn(self):
        return self.pwm

    def is_kick(self):
        return self.kick_note

    # PRINT
    def __str__( self ) :
        string = '('
        string += 'start time: ' + str(self.get_start_time())
        string += ', end time: ' + str(self.get_end_time())
        string += ', is_kick: ' + str(self.is_kick())
        string += ', frequency: ' + str(self.get_frequency())
        string += ', amplitude: ' + str(self.get_amplitude())
        string += ')'
        return string
