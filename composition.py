'''
COMPOSITION class
a composition is a collection of notes for one instrument
'''
import numpy as np
import note
from note import Note
import scale
import utilities

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

    def crush_notes( self ) :
        for note in self.notes :
            closest = utilities.find_closest( self.scale, note.get_frequency() )
            note.set_frequency( closest )

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
            
    def average_amplitude( self, notes ) :
        amplitude = 0
        for note in notes :
            amplitude += note.get_amplitude()
            
        return amplitude/len(notes)
            
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

    def unify_notes( self ) :
        decreased = False
        si = 0
        for i, note in enumerate(self.notes) :
            if note.get_amplitude() > self.notes[i-1].get_amplitude() * 1.10 :
                if decreased == True :
                    ei = i
                    self.merge_note_frequencies( self.notes[si:ei] )
                    si = i

                    decreased = False
            else :
                decreased = True
                
        self.remove_duplicates( )

    def high_pass_filter( self, gate ) :
        for i, note in enumerate(self.notes) :
            if note.get_frequency() < gate :
                frequency = 0
                if self.notes[i-1].get_frequency() :
                    frequency = self.notes[i-1].get_frequency()
                else :
                    frequency = self.notes[i+1].get_frequency()

                note.set_frequency( frequency )

    def low_pass_filter( self, gate ) :
        for i, note in enumerate(self.notes) :
            if note.get_frequency() > gate :
                frequency = 0
                if self.notes[i-1].get_frequency() :
                    frequency = self.notes[i-1].get_frequency()
                else :
                    frequency = self.notes[i+1].get_frequency()

                note.set_frequency( frequency )
                
    def limiter( self, limit ) :
        for i, note in enumerate(self.notes) :
            if note.get_frequency() > limit :
                note.set_frequency( limit )