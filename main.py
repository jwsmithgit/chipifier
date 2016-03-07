import sonic_scanner
import retro_conformer
import wave_generator

if __name__ == "__main__" :
    composition = sonic_scanner.scan( 'sound.wav' )

    #print( composition )
    composition.crush_notes()
    wave_generator.generate( composition )
