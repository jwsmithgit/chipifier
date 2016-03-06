Changes

transcriber.py
input - wave file
output - midi file(s)
takes audio, and creates a midi representation of the sounds in that audio

nesmidi.py
input - midi file(s)
output - midi file(s)
takes midi file(s), makes the midi notes  in those files conform to nes sound chip restrictions, applying tricks

generatesound.py
input - midi file(s)
output - wave file
take midi file(s), create a wave file using sounds that mimic the nes sound chip channels