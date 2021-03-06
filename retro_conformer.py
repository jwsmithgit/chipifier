
"""
Class containing functions used to alter the note list in the composition object.
Applying NES tricks to composition objects
"""

import scale
from composition import Composition
from note import Note
import utilities

# apply pulse modulation by splitting each note into a set amount
# then apply each pulse width value to each
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

# pwm enumerator function
def get_pwm_val(x):
    if x%4 == 0:
        return .5
    if x%4 == 1 or x%4 == 3:
        return .25
    if x%4 == 2:
        return .125
       
# pulse width mod that rotates through pulse width for set amount of time
# pulse width is changed over time and applied to whatever notes fall in that time
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

# apply reverb to notes by creating new channel 2 composition
# blank note at start, all notes are shifted by delay amount
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

# for each kick note in composition, cut off end of note before kick note
# have the the frequency start high and descend to the beat note frequency
def kick_drum_line(composition, drop_number):
    new_note_list = []
    duration = 44100 / 8
    drop_increment = duration / drop_number

    for i, note in enumerate(composition.get_notes()):
        effect_start_time = note.get_start_time() - duration
        effect_end_time = note.get_start_time()
        if effect_start_time < 0 :
            new_note_list.append(note)
            continue

        if i != 0:
            if note.is_kick():
                rollback = 0
                indices_in_notes_list = len(new_note_list) - 1

                #keep rolling back until "in drop time" notes are popped off
                while True:
                    last_note = new_note_list[-1]
                    if last_note.get_start_time() > (last_note.get_end_time() - duration):
                        new_note_list.pop()

                    else:
                        break

                last_note = new_note_list[-1]
                last_note.set_end_time(effect_start_time)

                scale = composition.get_scale()
                closest = utilities.find_closest(scale, note.get_frequency())
                index = scale.index(closest) + drop_number
                ampl = note.get_amplitude()

                for x in range(0, drop_number):
                    new_s_time = int(effect_start_time + x * drop_increment)
                    new_e_time = int(effect_start_time + (x+1) * drop_increment)
                    new_freq = scale[index]

                    nn = Note(new_s_time, new_e_time, new_freq, ampl)
                    nn.set_kick(True)

                    new_note_list.append(nn)
                    index -=1

                new_note_list.append(note)
                   
            else:
                new_note_list.append(note)

    composition.notes = new_note_list

# echo by placing a smaller amplitude note after the note that comes after each note
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

            ahead_ampl = ampl * 1/2
            ahead_freq = freq
            ahead_real_duration = (note.get_end_time() - note.get_start_time()) / 2

    composition.notes = new_note_list


if __name__ == "__main__" :
    print("NESMIDI")
