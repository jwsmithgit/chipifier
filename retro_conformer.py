"""
Class containing functions used to alter the note list in the composition object.
Applying NES tricks to composition objects
"""

import note
import scale

def split_composition_notes(composition):
    notes = composition.notes
    pwm_notes = []
    for c_note in notes:
        increment = ( c_note.get_end_time() - c_note.get_start_time() ) / 4
        for x in range(0,4):
            new_start = int(c_note.get_start_time() + x * increment)
            new_end =  int(c_note.get_start_time() + (x+1) * increment)
            new_note = note.Note(new_start, new_end, c_note.get_frequency(), c_note.get_amplitude(),get_pwn_val(x))
            pwm_notes.append(new_note)
    composition.notes = pwm_notes

def get_pwn_val(x):
    if x == 0:
        return 50.0
    if x == 1 or x == 3:
        return 25.0
    if x == 2:
        return 12.5

def reverb_composition(composition, loudness_factor, delay):
    for note in composition.notes:
        delay_start = note.get_start_time() - delay
        delay_end = note.get_end_time() - delay
        if delay_start < 0:
            composition.remove_note(note)
        else:
            note.set_start_time(delay_start)
            note.set_end_time(delay_end)
            note.set_amplitude( note.get_amplitude() * loudness_factor )

def kick_drum_line(composition, chopoff, drop_number):
    for i in range(0, len(composition.notes))
        if composition.notes[i].is_kick() and i !=0:
            slot_start_time = composition.notes[i].get_start_time() - chopoff
            slot_end_time = composition.notes[i].get_start_time()
            increment = (slot_end_time - slot_start_time) / drop_number
            composition.notes[i].set_end_time(slot_start_time)
            new_amplitude = composition.notes[i].get_amplitude() * 2
            amplitude_decrease = 1 / drop_number
            drop_notes = []
            scale = composition.get_scale()
            index = scale.index(composition.notes[i].get_frequency()) + 10
            for x in range(0, drop_number):
                drum_note_start = slot_start_time + x * increment
                drum_note_end = slot_start_time + (x+1) * increment
                drum_note_freq = scale[index]
                drum_note_amplitude = new_amplitude
                index -= 1
                new_amplitude -= amplitude_decrease
                drop_notes.append(note.Notes(drum_note_start, drum_note_end, drum_note_freq, drum_note_amplitude))
            




if __name__ == "__main__" :
    print("NESMIDI")
