
"""
Class containing functions used to alter the note list in the composition object.
Applying NES tricks to composition objects
"""

import scale
from note import Note
import utilities

def split_composition_notes(composition):
    notes = composition.notes
    pwm_notes = []
    for c_note in notes:
        increment = ( c_note.get_end_time() - c_note.get_start_time() ) / 4
        for x in range(0,4):
            new_start = int(c_note.get_start_time() + x * increment)
            new_end =  int(c_note.get_start_time() + (x+1) * increment)
            new_note = Note(new_start, new_end, c_note.get_frequency(), c_note.get_amplitude(),get_pwn_val(x))
            pwm_notes.append(new_note)
    composition.notes = pwm_notes

def get_pwn_val(x):
    if x == 0:
        return .5
    if x == 1 or x == 3:
        return .25
    if x == 2:
        return .125

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
    new_note_list = []
    for i, note in enumerate(composition.notes):
        if i == 0:
            continue
        else:
            if note.is_kick():
                prev_note = composition.notes[i-1]
                slot_start_time = prev_note.get_end_time() - chopoff
                slot_end_time = note.get_start_time()
                prev_note.set_end_time(slot_start_time)

                increment = (slot_end_time - slot_start_time) / drop_number
                new_ampl = note.get_amplitude() * 2
                amplitude_decrease =(new_ampl - note.get_amplitude()) / drop_number

                scale = composition.get_scale()
                closest = utilities.find_closest(scale, composition.notes[i].get_frequency())
                index = scale.index(closest) + 10

                for x in range(0, drop_number):
                    new_s_time = int(slot_start_time + x * increment)
                    new_e_time = int(slot_start_time + (x+1) * increment)
                    new_freq = scale[index]
                    new_note_list.append( Note(new_s_time, new_e_time, new_freq, new_ampl) )
                    new_ampl -= amplitude_decrease
                    index -=1
                new_note_list.append(note)
            else:
                new_note_list.append(note)
    composition.notes = new_note_list

def single_channel_echo(composition):
    new_note_list = []
    previous_end = 0
    ahead_note = Note()
    for i, note in enumerate(composition.notes):
        if i == 0 :
            end = note.get_end_time() / 2
            new_ampl = note.get_amplitude() / 2
            new_note_list.append( Note(0, end, note.get_frequency(), note.get_amplitude) )
            ahead_note = Note(0, 0, note.get_frequency(), new_ampl)
            ahead_note.set_kick(True)
            continue
        else:
            #set echo note
            last_end = new_note_list[-1].get_end_time()
            new_end = last_end + (ahead_note.get_start_time() - ahead_note.get_end_time()) / 2
            ahead_note.set_end_time(new_end)
            ahead_note.set_start_time(last_end)
            ahead_note.set_kick(True)
            ahead_note.set_amplitude( ahead_note.get_amplitude() / 2)
            new_note_list.append(ahead_note)

            #set note
            last_end = new_end
            new_end = last_end + (note.get_start_time() - note.get_end_time()) / 2
            freq = note.get_frequency()
            ampl = note.get_amplitude()
            new_note_list.append(Note(last_end, new_end, freq, ampl))

            ahead_note = note
    composition.notes = new_notes_list


if __name__ == "__main__" :
    print("NESMIDI")
