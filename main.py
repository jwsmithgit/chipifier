import sonic_scanner
import retro_conformer
import wave_generator

def output_to_file( var ) :
    f = open( 'file.txt', 'w' )
    f.write( str(var) )
    f.close()
    return

if __name__ == "__main__" :
    composition = sonic_scanner.scan( 'sound.wav' )

    #print( composition )
    composition.crush_notes()
    composition.unify_notes()
    composition.high_pass_filter(1000)
    #print( composition )
    output_to_file( composition )
    wave_generator.generate( composition )
