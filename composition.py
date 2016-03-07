'''
COMPOSITION class
a composition is a collection of notes for one instrument
'''

import note
import math

# need function to crush to musical notes
# A0 is 27.5 all steps are multiplied by 12root(2) or 1.0594 steps up until A9 14080
# see monophonic pitch slide 24
def music_notes( ) :
    notes = [ 27.5 ]
    while notes[-1] <= 14080 :
        notes.append( notes[0] * (math.pow(2,len(notes)/12)) )

    return notes

def find_closest( li, value ) :
    if value < li[0] :
        return li[0]
    if value > li[-1] :
        return li[-1]

    mid = len(li) // 2
    a = li[ mid ]
    b = li[ mid + 1 ]

    if value > a and value < b :
        a_diff = value - a
        b_diff = b - value
        if a_diff < b_diff :
            return a
        else :
            return b

    if value < a :
        return find_closest( li[:mid], value )

    else :
        return find_closest( li[mid:], value )

class Composition :
    def __init__( self, notes=[ ] ) :
        self.tempo = -1
        self.notes = notes
        self.music_notes = music_notes( )

    # add notes to composition
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
        for note in self.notes :
            print(note)
        return ''

    # sort by start times
    def sort_by_start_times( self ) :
        notes = sorted(self.notes, key = lambda note: int(note[0]))

    def crush_notes( self ) :
        for note in self.notes :
            closest = find_closest( self.music_notes, note.frequency )
            note.set_frequency( closest )
