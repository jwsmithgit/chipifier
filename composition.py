'''
COMPOSITION class
a composition is a collection of notes for one instrument
'''
import numpy as np
import note
from note import Note
import scale
import utilities
import random

class Composition :
    def __init__( self ) :
        self.channel = 1
        self.tempo = -1
        self.notes = [ ]
        self.scale = scale.western_scale() #scale.get_scale( channel )

    # SETTERS
    def set_channel( self, channel ) :
        self.channel = channel 
    
    def set_tempo( self, tempo ) :
        self.tempo = tempo
    
    def set_notes( self, notes ) :
        self.notes = notes
        
    def set_scale( self, channel ) :
        self.scale = scale.get_scale( channel )
        
    # GETTERS
    def get_channel( self ) : 
        return self.channel
    
    def get_tempo( self ) :
        return self.tempo
        
    def get_notes( self ) :
        return self.notes
        
    def get_scale( self ) :
        return self.scale

    # add note to composition
    def add_note( self, note ) :
        self.notes.append(note)

    # add notes to composition
    def add_notes( self, notes ) :
        self.notes.extend( notes )

    # remove a note from the composition
    def remove_note( self, note ) :
        self.notes.remove( note )

    # prints a pretty composition
    def __str__( self ) :
        string = ""
        for note in self.notes :
            string += str(note) + '\n'
        return string

    # sort by start times
    def sort_by_start_times( self ) :
        notes = sorted(self.notes, key = lambda note: int(note[0]))
        
    # set all notes to pulse width
    def set_pulse_widths( self, pwm ) :
        for note in self.notes :
            note.set_pwm( pwm )

    # set all notes to closest value in scale
    def crush_notes( self ) :
        for note in self.notes :
            closest = utilities.find_closest( self.scale, note.get_frequency() )
            note.set_frequency( closest )

    # set list of notes to the most common frequency occurence
    def merge_note_frequencies( self, notes ) :
        if not notes :
            return

        frequencies = [ ]
        for note in notes :
            frequencies.append( note.get_frequency() )

        frequency_counts = np.bincount( frequencies )
        new_frequency = np.argmax( frequency_counts )

        for note in notes :
            note.set_frequency( new_frequency )
            
    # get average amplitude of set of notes
    def average_amplitude( self, notes ) :
        amplitude = 0
        for note in notes :
            amplitude += note.get_amplitude()
            
        return amplitude/len(notes)
            
    # remove adjacent notes of the same frequency and replaces with single note
    def remove_duplicates( self ) :
        notes = [ ]
        
        si = 0
        for i,note in enumerate(self.notes[:-1]) :
            if self.notes[i].get_frequency() != self.notes[i+1].get_frequency() :
                ei = i+1
                
                amplitude = self.average_amplitude( self.notes[si:ei] )
                notes.append( Note( self.notes[si].get_start_time(), self.notes[ei].get_start_time(), self.notes[si].get_frequency(), amplitude) )
                
                si = ei
                
        self.notes = notes

    # if note amplitude is more than last note amplitude
    # grab all notes since last time that happened and considers that a note
    # the notes are merged into a single note
    def unify_notes( self ) :
        decreased = False
        si = 0
        for i, note in enumerate(self.notes) :
            if self.notes[i].get_amplitude() > self.notes[i-1].get_amplitude() :
                if decreased == True :
                    ei = i
                    self.merge_note_frequencies( self.notes[si:ei] )
                    si = i

                    decreased = False
            else :
                decreased = True
                
        self.remove_duplicates( )
        
    # if note amplitude is more than last 10 notes average note amplitude
    # grab all notes since last time that happened and considers that a note
    # the notes are merged into a single note
    def better_unify_notes( self ) :
        notes = self.get_notes()
        decreased = False
        si = 0
        amplitudes = [ ]
        average = 0
        
        for i, note in enumerate(notes) :
        
            average = average * len(amplitudes)
            if ( len(amplitudes) == 10 ) :
                average -= amplitudes[0]
                amplitudes = amplitudes[1:]
                
            amplitudes.append( notes[i].get_amplitude() )
            average += amplitudes[-1]
            average = average / len(amplitudes)
            
            if notes[i].get_amplitude() > average:
                if decreased == True :
                    ei = i
                    self.merge_note_frequencies( notes[si:ei] )
                    si = i

                    decreased = False
            else :
                decreased = True
                
        self.remove_duplicates( )

    # if note frequecny is less than gate frequency, set to previous note frequency
    def high_pass_filter( self, gate ) :
        for i, note in enumerate(self.notes) :
            if note.get_frequency() < gate :
                frequency = 0
                if self.notes[i-1].get_frequency() :
                    frequency = self.notes[i-1].get_frequency()
                else :
                    frequency = self.notes[i+1].get_frequency()

                note.set_frequency( frequency )

    # if note frequecny is more than gate frequency, set to previous note frequency
    def low_pass_filter( self, gate ) :
        for i, note in enumerate(self.notes) :
            if note.get_frequency() > gate :
                frequency = 0
                if self.notes[i-1].get_frequency() :
                    frequency = self.notes[i-1].get_frequency()
                else :
                    frequency = self.notes[i+1].get_frequency()

                note.set_frequency( frequency )
               
    # if note frequecny is more than limit frequency, set to limit frequency
    def limiter( self, limit ) :
        for i, note in enumerate(self.notes) :
            if note.get_frequency() > limit :
                note.set_frequency( limit )
    
    # if note frequecny is less than limit frequency, set to limit frequency
    def reverse_limiter( self, limit ) :
        for i, note in enumerate(self.notes) :
            if note.get_frequency() < limit :
                note.set_frequency( limit )

    #for random kicks (1/6 odds)
    def set_random_kicks( self ):
        for note in self.notes:
            val = random.randint(1,6)
            if val == 4:
                note.set_kick(True)
