'''
COMPOSITION class
a composition is a collection of notes for one instrument
'''

import note

class Composition :
    def __init__( self, notes=[ ] ) :
        self.tempo = -1
        self.notes = notes

    # add notes to composition
    def add_note( self, note ) :
        self.notes += note

    # add notes to composition
    def add_notes( self, notes ) :
        self.notes += notes

    # remove a note from the composition
    def remove_note( self, note ) :
        self.notes.remove( note )

    # prints a pretty composition
    def __str__( self ) :
        string = '['
        for note in self.notes :
            print(note)
        string += ']'
        return string

    # sort by start times
    def sort_by_start_times( self ) :
        notes = sorted(self.notes, key = lambda note: int(note[0]))
