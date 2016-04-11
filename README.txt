Changes

transcriber.py
input - wave file
output - composition object
takes audio, and creates a note representation of the sounds in that audio

nesmidi.py
input - composition object
output - composition object
takes notes, makes the notes  in those files conform to nes sound chip restrictions, applying tricks

generatesound.py
input - composition object
output - wave file
take notes, create a wave file using sounds that mimic the nes sound chip channels