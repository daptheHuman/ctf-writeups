import mido  # Importing the mido library

def print_program_change_chars(midi_file_path):
    # Load the MIDI file
    midi = mido.MidiFile(midi_file_path)
    
    # List to hold all program change characters
    program_chars = []
    
    # Iterate through all messages in all tracks
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'program_change':
                # Convert program number to character and add to the list
                print(msg.program, chr(msg.program))
                program_char = chr(msg.program)
                program_chars.append(program_char)
                 
    # Print all program change characters
    print("Program Change Characters:")
    print(''.join(program_chars))

# Specify the path to your MIDI file
midi_file_path = 'coolsong2.mid'
print_program_change_chars(midi_file_path)
