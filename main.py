import librosa
import pretty_midi

# Load the whistled audio
audio_path = "new_music.mp3"
y, sr = librosa.load(audio_path)

# Estimate the pitches using librosa's piptrack
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
pitch_track = []

# Extract the dominant pitch at each frame
for i in range(pitches.shape[1]):
    index = magnitudes[:, i].argmax()
    pitch = pitches[index, i]
    if pitch > 0:
        pitch_track.append(pitch)
    else:
        pitch_track.append(0)

# Convert pitch to MIDI notes, filtering zeros
midi_notes = [librosa.hz_to_midi(p) if p > 0 else 0 for p in pitch_track]

# Smooth and clean up the notes for MIDI
cleaned_notes = []
threshold = 0.5  # Change sensitivity if needed
prev_note = None
for note in midi_notes:
    if note > 0:
        note = int(round(note))
        if note != prev_note:
            cleaned_notes.append(note)
            prev_note = note

# Create a PrettyMIDI object
midi = pretty_midi.PrettyMIDI()
instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

# Add notes with some duration
start_time = 0
duration = 0.4  # seconds per note
for note_number in cleaned_notes:
    note = pretty_midi.Note(velocity=100, pitch=note_number, start=start_time, end=start_time + duration)
    instrument.notes.append(note)
    start_time += duration

midi.instruments.append(instrument)

# Save MIDI file
midi_path = "your_music.mid"
midi.write(midi_path)

midi_path
