import note

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
        return .5
    if x == 1 or x == 3:
        return .25
    if x == 2:
        return .125

def reverb_composition(composition, loudness_factor, delay):
    note_ = note.Note(0, delay, 0, 0)
    composition.notes.insert(0, note_)
    
    for note_ in composition.notes:
        delay_start = note_.get_start_time() + delay
        delay_end = note_.get_end_time() + delay
        #if delay_start < 0:
        #    composition.remove_note(note)
        #else:
        note_.set_start_time(delay_start)
        note_.set_end_time(delay_end)
        note_.set_amplitude( note_.get_amplitude() * loudness_factor )
        
    return composition

if __name__ == "__main__" :
    print("NESMIDI")
