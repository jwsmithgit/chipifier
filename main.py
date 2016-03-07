import sonic_scanner
import retro_conformer
import wave_generator

if __name__ == "__main__" :
    composition = sonic_scanner.scan( 'sound1.wav' )
    wave_generator.generate( composition )
