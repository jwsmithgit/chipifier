
"""
Class containing functions used to alter the note list in the composition object.
Applying NES tricks to composition objects
"""

import scale
from composition import Composition
from note import Note
import utilities

def split_composition_notes(composition, split):
    notes = composition.get_notes()
    pwm_notes = []
    for c_note in notes:
        increment = ( c_note.get_end_time() - c_note.get_start_time() ) / split
        for x in range(0,split):
            new_start = int(c_note.get_start_time() + x * increment)
            new_end =  int(c_note.get_start_time() + (x+1) * increment)
            new_note = Note(new_start, new_end, c_note.get_frequency(), c_note.get_amplitude(),get_pwm_val(x))
            pwm_notes.append(new_note)
    composition.notes = pwm_notes

def get_pwm_val(x):
    if x%4 == 0:
        return .5
    if x%4 == 1 or x%4 == 3:
        return .25
    if x%4 == 2:
        return .125
        
def pulse_width_mod( composition, pulse_width ) :
    notes = composition.get_notes()
    new_composition = Composition()
    
    final_end_time = notes[-1].get_end_time()
    time = 0
    pwm = 0
    cni = 0 # composition note index
    while time < final_end_time :
        end_time = time + pulse_width
        
        while cni < len(notes) and notes[cni].get_end_time() < end_time :
            note = Note()
            note.set_start_time( time )
            note.set_end_time( notes[cni].get_end_time() )
            note.set_frequency( notes[cni].get_frequency() )
            note.set_amplitude( notes[cni].get_amplitude() )
            note.set_pwm( get_pwm_val( pwm ) )
            
            new_composition.add_note( note )
            time += notes[cni].get_end_time() - notes[cni].get_start_time()
            cni += 1
            
        if cni == len(notes) :
            break
        
        note = Note()
        note.set_start_time( time )
        note.set_end_time( end_time )
        note.set_frequency( notes[cni].get_frequency() )
        note.set_amplitude( notes[cni].get_amplitude() )
        note.set_pwm( get_pwm_val( pwm ) )
        
        new_composition.add_note( note )
        time = end_time
        pwm = (pwm + 1) % 4
        
    composition.set_notes( new_composition.get_notes() )

def reverb_composition(composition, loudness_factor, delay):
    for note in composition.get_notes():
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
    for i, note in enumerate(composition.get_notes()):
        if i != 0:
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
    ahead_freq = 0
    ahead_ampl = 0
    ahead_real_duration = 0
    for i, note in enumerate(composition.get_notes()):
        if i == 0 :
            ampl = note.get_amplitude()
            freq = note.get_frequency()
            start = 0
            end = note.get_end_time() / 2
            new_note_list.append(Note(start, end, freq, ampl))

            ahead_freq = freq
            ahead_ampl = ampl / 2
            ahead_real_duration = end
        else:
            ampl = note.get_amplitude()
            freq = note.get_frequency()
            start = new_note_list[-1].get_end_time()
            end = start + (note.get_end_time() - note.get_start_time()) / 2
            new_note_list.append(Note(start, end, freq, ampl))

            last = new_note_list[-1].get_end_time()
            new_note_list.append(Note(last, last + ahead_real_duration, ahead_freq, ahead_ampl))

            ahead_ampl = ampl / 2
            ahead_freq = freq
            ahead_real_duration = (note.get_end_time() - note.get_start_time()) / 2

    composition.notes = new_note_list


if __name__ == "__main__" :
    print("NESMIDI")
