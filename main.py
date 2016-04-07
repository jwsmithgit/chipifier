import argparse
import copy

import sonic_scanner
import retro_conformer
import wave_generator

import pylab as pl

def output_to_file( filename, var ) :
    f = open( filename, 'w' )
    f.write( str(var) )
    f.close()
    return

def create_parser() :
    parser = argparse.ArgumentParser()
    parser.add_argument('--allin', action="store", dest="allin", default=None, help="all instruments track file")

    parser.add_argument('--lead1', action="store", dest="lead1", default=None, help="1: first lead track file")
    parser.add_argument('--lead2', action="store", dest="lead2", default=None, help="2: second lead track file")
    parser.add_argument('--bass', action="store", dest="bass", default=None, help="3: bass track file")
    parser.add_argument('--drums', action="store", dest="drums", default=None, help="4: drum track file")

    parser.add_argument('--outfile', action="store", dest="outfile", default='chiptune.wav', help="the resulting output file")

    parser.add_argument('--l1voice', action="store", dest="l1voice", type=int, choices=(1,2,3), default=1, help="what voice lead1 will use")
    parser.add_argument('--l2voice', action="store", dest="l2voice", type=int, choices=(1,2,3), default=2, help="what voice lead2 will use")
    parser.add_argument('--dvoice', action="store", dest="dvoice", type=int, choices=(1,2), default=1, help="what voice drums will use")

    parser.add_argument('--reverb', action="store_true", dest="reverb", help="use reverb effect on lead 1, replaces lead 2")
    parser.add_argument('--echo', action="append", dest="echo", type=int, choices=(1,2), default=[], help="which lead will use echo effect")
    parser.add_argument('--mod', action="append", dest="mod", type=int, choices=(1,2), default=[], help="which lead will use duty cycle modulation effect")
    parser.add_argument('--arp', action="append", dest="arp", type=int, choices=(1,2), default=[], help="which lead will use arpeggio effect")

    parser.add_argument('--gendrums', action="store_true", dest="gendrums", help="generate drums")
    parser.add_argument('--trikick', action="store_true", dest="trikick", help="use tringle wave for drum kick")

    parser.add_argument('--polydetect', action="append", dest="polydetect", type=int, choices=(1,2,3,4), default=[], help="which instruments will use polyphonic detection")
    parser.add_argument('--dywindows', action="store_true", dest="dywindows", help="use dynamic windows for frequency detection")
    parser.add_argument('--freqdetect', action="store", dest="freqdetect", choices=('fft','autocorr'), default='autocorr', help="use fft or autocorrelation for autocorrelation")

    parser.add_argument('--notesmooth', action="store_true", dest="notesmooth", help="use note smoother")
    parser.add_argument('--hipass', action="store_true", dest="hipass", help="use high pass filter")
    parser.add_argument('--hipassval', action="store", dest="hipassval", type=int, default=10, help="specify high pass filter value")
    parser.add_argument('--lopass', action="store_true", dest="lopass", help="use low pass filter")
    parser.add_argument('--lopassval', action="store", dest="lopassval", type=int, default=10000, help="specify low pass filter value")

    return parser

if __name__ == "__main__" :
    parser = create_parser()
    args = parser.parse_args()

    # all the files to process frequencies
    wave_files = [(1,'piano_sound.wav')]
    if( args.allin ) :
        wave_files.append( (0, args.allin) )

    else :
        if ( args.lead1 ) :
            wave_files.append( (1, args.lead1) )

        if ( args.lead2 ) :
            wave_files.append( (2, args.lead2) )

        if ( args.bass ) :
            wave_files.append( (3, args.bass) )

        if ( args.drums ) :
            wave_files.append( (4, args.drums) )

    # get notes for each file
    compositions = [ ] 
    for tup in wave_files :
        channel = tup[0]
        wave_file = tup[1]
        
        
        '''
        #OSS
        beats = sonic_scanner.beat_scan( wave_file )
        composition = sonic_scanner.note_scan( wave_file, beats, channel )
        composition.crush_notes( )
        composition.low_pass_filter( 1000 )
        composition.high_pass_filter( 50 )
        '''
        
        
        '''
        basic amplitude detection
        beats = sonic_scanner.onset_scan( wave_file )
        composition = sonic_scanner.note_scan( wave_file, beats, channel )
        '''
        
        
        composition = sonic_scanner.basic_note_scan( wave_file, channel )
        composition.crush_notes( )
        composition.unify_notes()
        composition.low_pass_filter( 1000 )
        
        
        
        if ( args.notesmooth ) :
            composition.unify_notes()

        if ( args.hipass ) :
            composition.high_pass_filter( args.hipassval )

        if ( args.lopass ) :
            composition.low_pass_filter( args.lopassval )
        

        output_to_file( 'file.txt', composition )
        compositions.append( composition )
        
    for composition in compositions:
        if composition.channel == 1:
            if ( args.mod == 1 ) :
                retro_conformer.split_composition_notes(composition)
            if ( args.reverb == 1 ) :
                composition_channel2 = copy.deepcopy(composition)
                composition_channel2.set_channel( 2 )
                composition_channel2 = retro_conformer.reverb_composition(composition_channel2, 0.5, 44100/5)
                compositions.append(composition_channel2)
                
        if composition.channel == 2:
            if ( args.mod == 2 ) :
                retro_conformer.split_composition_notes(composition)
    
    # get notes for each file
    waves = []
    for composition in compositions :
        waves.append( wave_generator.generate( composition ) )
        
    mix = wave_generator.mix_waves( waves )
    params = (1, 2, 44100, len(mix), 'NONE', 'not compressed')
    wave_generator.write_to_file(mix, 'chiptune.wav', params)
    