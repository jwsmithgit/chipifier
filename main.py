import sonic_scanner
import retro_conformer
import wave_generator

def output_to_file( var ) :
    f = open( 'file.txt', 'w' )
    f.write( str(var) )
    f.close()
    return

if __name__ == "__main__" :
    composition = sonic_scanner.beat_scan( 'piano_sound.wav' )
    composition.detect_beats()

    composition = sonic_scanner.note_scan( 'piano_sound.wav', composition )
    composition.notes = composition.beat_notes

    #print( composition )
    #composition.unify_notes()
    composition.crush_notes()
    #composition.high_pass_filter(1000)
    #print( composition )
    output_to_file( composition )
    wave_generator.generate( composition )
