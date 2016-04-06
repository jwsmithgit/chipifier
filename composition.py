'''
COMPOSITION class
a composition is a collection of notes for one instrument
'''
import numpy as np
import note
import math
import scale
import utilities

def find_beat_locations( wave_window_averages_list ):
    beat_note_list = []
    count = 1;
    previous_windows_average = 0

    #gradual average for first set of windows
    for window_average in wave_window_averages_list:
        if count == 1:
            count += 1
            previous_windows_average = window_average
            continue
        if count > 40:
            break

        # if current note average is greater than avg of previous windows
        if( window_average > previous_windows_average ) :
            beat_note = note.Note( start_time = 1024 * count )
            beat_note_list.append( beat_note )

        previous_window_average = ( previous_windows_average * count )
        count += 1
        previous_notes_average = ( previous_windows_average + window_average ) / count

    count = 1
    #full size window detection of beats for the rest of the windows
    for window_average in wave_window_averages_list:
        if( count <= 41 ) :
            count += 1
            continue
        if( window_average > previous_windows_average ) :
           beat_note = note.Note( start_time = 1024 * count )
           beat_note_list.append( beat_note )

        previous_window_average = ( previous_windows_average * count )
        count += 1
        previous_notes_average = ( previous_windows_average + window_average ) / count


    #add end time for each note (=start time of the next)
    next = 1
    for beat_note in beat_note_list:
        if( next == len(beat_note_list) ) :
            beat_note.set_end_time( beat_note.get_start_time() + 1024 ) #could potentially change this (end time of last note)
            break
        beat_note.set_end_time( beat_note_list[next].get_start_time() )
        next += 1

    return beat_note_list


class Composition :
    def __init__( self, notes=[ ], channel ) :
        self.tempo = -1
        self.notes = notes
        self.scale = scale.western_scale( )
        self.raw_window_averages = [ ]
        self.beat_notes = [ ]
        self.channel = channel

    #add raw wave values
    def add_raw_window_average( self, value):
        self.raw_window_averages.append(value)

    # add note to composition
    def add_note( self, note ) :
        self.notes.append(note)

    # add notes to composition
    def add_notes( self, notes ) :
        self.notes += notes

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
            closest = utilities.find_closest( self.scale, note.frequency )
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

    def high_pass_filter( self, gate ) :
        for i, note in enumerate(self.notes) :
            if note.get_frequency() > gate :
                frequency = 0
                if self.notes[i-1].get_frequency() :
                    frequency = self.notes[i-1].get_frequency()
                else :
                    frequency = self.notes[i+1].get_frequency()

                note.set_frequency( frequency )

    def low_pass_filter( self, gate ) :
        for i, note in enumerate(self.notes) :
            if note.get_frequency() < gate :
                frequency = 0
                if self.notes[i-1].get_frequency() :
                    frequency = self.notes[i-1].get_frequency()
                else :
                    frequency = self.notes[i+1].get_frequency()

                note.set_frequency( frequency )

    def detect_beats( self ):
        self.beat_notes = find_beat_locations(self.raw_window_averages)
