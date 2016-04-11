import argparse

import sonic_scanner
import retro_conformer
import wave_generator

import pylab as pl

from composition import Composition
from note import Note

def output_to_file( filename, var ) :
    f = open( filename, 'w' )
    f.write( str(var) )
    f.close()
    return

def create_parser() :
    parser = argparse.ArgumentParser()
    parser.add_argument('--allin', action="store", dest="allin", default=None, help="NOT YET SUPPORTED all instruments track file")

    parser.add_argument('--lead1', action="store", dest="lead1", default=None, help="1: first lead track file")
    parser.add_argument('--lead2', action="store", dest="lead2", default=None, help="2: second lead track file")
    parser.add_argument('--bass', action="store", dest="bass", default=None, help="3: bass track file")
    parser.add_argument('--drums', action="store", dest="drums", default=None, help="4: drum track file")

    parser.add_argument('--outfile', action="store", dest="outfile", default='chiptune.wav', help="the resulting output file")

    parser.add_argument('--l1voice', action="store", dest="l1voice", type=int, choices=(1,2,3), default=1, help="what voice lead1 will use, 1: .5, 2: .25, 3: .125")
    parser.add_argument('--l2voice', action="store", dest="l2voice", type=int, choices=(1,2,3), default=1, help="what voice lead2 will use, 1: .5, 2: .25, 3: .125")
    parser.add_argument('--dvoice', action="store", dest="dvoice", type=int, choices=(1,2), default=1, help="NOT YET SUPPORTED what voice drums will use")

    parser.add_argument('--reverb', action="store_true", dest="reverb", help="use reverb effect on lead 1, replaces lead 2")
    parser.add_argument('--echo', action="append", dest="echo", type=int, choices=(1,2), default=[], help="which lead will use echo effect")
    parser.add_argument('--mod', action="append", dest="mod", type=int, choices=(1,2), default=[], help="which lead will use duty cycle modulation effect")
    parser.add_argument('--arp', action="append", dest="arp", type=int, choices=(1,2), default=[], help="NOT YET SUPPORTED which lead will use arpeggio effect")

    parser.add_argument('--gendrums', action="store_true", dest="gendrums", help="NOT YET SUPPORTED generate drums")
    parser.add_argument('--trikick', action="store_true", dest="trikick", help="NOT YET SUPPORTED use tringle wave for drum kick")

    '''
    parser.add_argument('--polydetect', action="append", dest="polydetect", type=int, choices=(1,2,3,4), default=[], help="NOT YET SUPPORTED which instruments will use polyphonic detection")
    parser.add_argument('--dywindows', action="store_true", dest="dywindows", help="NOT YET SUPPORTED use dynamic windows for frequency detection")
    parser.add_argument('--freqdetect', action="store", dest="freqdetect", choices=('fft','autocorr'), default='autocorr', help="use fft or autocorrelation for autocorrelation")
    '''
    
    '''
    parser.add_argument('--notesmooth', action="store_true", dest="notesmooth", help="use note smoother")
    parser.add_argument('--hipass', action="store_true", dest="hipass", help="NOT YET SUPPORTED use high pass filter")
    parser.add_argument('--hipassval', action="store", dest="hipassval", type=int, default=10, help="NOT YET SUPPORTED specify high pass filter value")
    parser.add_argument('--lopass', action="store_true", dest="lopass", help="NOT YET SUPPORTED use low pass filter")
    parser.add_argument('--lopassval', action="store", dest="lopassval", type=int, default=10000, help="NOT YET SUPPORTED specify low pass filter value")
    '''

    return parser

if __name__ == "__main__" :
    sampling_rate = 44100
    
    parser = create_parser()
    args = parser.parse_args()

    # all the files to process
    # TESTERS to avoid typing
    #wave_files = [(1,'sounds/l1.wav'),(2,'sounds/l2.wav'),(3,'sounds/b.wav'),(4,'sounds/d.wav')]
    #wave_files = [(1,'sounds/l1.wav')]
    #wave_files = [(2,'sounds/l2.wav')]
    wave_files = [(3,'sounds/b.wav')]
    #wave_files = [(4,'sounds/d.wav')]
    #wave_files = [(1,'real/ssgr.wav'),(2,'real/sssr.wav'),(3,'real/ssbr.wav'),(4,'real/ssdr.wav')]
    #wave_files = [(1,'real/wabgr.wav'),(2,'real/wabsr.wav'),(3,'real/wabbr.wav'),(4,'real/wabdr.wav')]
    #wave_files = [(1,'real/40rgr.wav'),(2,'real/40rsr.wav'),(3,'real/40rbr.wav'),(4,'real/40rdr.wav')]
    
    #wave_files = []

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
        
        # lead and bass processing
        if ( channel == 1 or channel == 2 or channel == 3 ) :
            composition = sonic_scanner.basic_note_scan( wave_file, channel )
            composition.crush_notes( )
            composition.better_unify_notes()
            composition.low_pass_filter( 1000 )
        # drum processing
        if ( channel == 4 ) :
            beats = sonic_scanner.beat_scan( wave_file, sampling_rate )
            composition = sonic_scanner.note_scan( wave_file, beats, channel )
            composition.reverse_limiter( 110 )
            composition.limiter( 7040 )
            composition.crush_notes( )
            
        # applying pulse widths
        if( channel == 1 ) :
            if ( args.l1voice == 1 ) :
                composition.set_pulse_widths(0.5)
            elif ( args.l1voice == 2 ) :
                composition.set_pulse_widths(0.25)
            elif ( args.l1voice == 3 ) :
                composition.set_pulse_widths(0.125)
        
        if ( channel == 2 ) :
            if ( args.l2voice == 1 ) :
                composition.set_pulse_widths(0.5)
            elif ( args.l2voice == 2 ) :
                composition.set_pulse_widths(0.25)
            elif ( args.l2voice == 3 ) :
                composition.set_pulse_widths(0.125)
        
        compositions.append( composition )
    
    for composition in compositions :
        if ( composition.get_channel() == 1 ):
            if ( 1 in args.echo ) :
                retro_conformer.single_channel_echo(composition)
            if ( 1 in args.mod ) :
                #retro_conformer.split_composition_notes(composition)
                retro_conformer.pulse_width_mod( composition, sampling_rate/8 )
            if ( args.reverb ) :
                # remove other channel 2 compositions
                for comp2 in compositions :
                    if comp2.get_channel() == 2 :
                        compositions.remove(comp2)
                        
                composition_channel2 = Composition()
                composition_channel2.set_channel( 2 )
                composition_channel2.add_notes( composition.get_notes() )
                retro_conformer.reverb_composition(composition_channel2, 0.5, sampling_rate/4)
                compositions.append(composition_channel2)
                
        if composition.get_channel() == 2:
            if ( 2 in args.echo ) :
                retro_conformer.single_channel_echo(composition)
            if ( 2 in args.mod ) :
                #retro_conformer.split_composition_notes(composition)
                retro_conformer.pulse_width_mod( composition, sampling_rate/8 )

        if composition.get_channel() == 3:
            if ( args.trikick ) : 
                retro_conformer.kick_drum_line(composition, 4)
                output_to_file( 'err.txt', composition )
    
    # get notes for each file
    waves = []
    for composition in compositions :
        waves.append( wave_generator.generate( composition, sampling_rate ) )
    mix = wave_generator.mix_waves( waves )
    
    # append .wav to filename if not there
    output_file = args.outfile
    if ( len(output_file) < 4 or output_file[-4:] != '.wav' ) :
        output_file += '.wav'
        
    params = (1, 2, sampling_rate, len(mix), 'NONE', 'not compressed')
    wave_generator.write_to_file(mix, output_file, params)
    