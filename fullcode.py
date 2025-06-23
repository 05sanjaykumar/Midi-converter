import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import pretty_midi
from scipy.signal import medfilt

def extract_melody_improved(audio_path):
    # Load the whistled audio
    y, sr = librosa.load(audio_path)
    
    # Use a better pitch tracking method
    # f0 uses a more robust algorithm for monophonic pitch detection
    f0, voiced_flag, voiced_probs = librosa.pyin(y, 
                                                 fmin=librosa.note_to_hz('C4'), 
                                                 fmax=librosa.note_to_hz('C7'),
                                                 sr=sr)
    
    # Apply median filter to smooth out pitch track
    f0_filtered = medfilt(f0, kernel_size=5)
    
    # Convert to times
    times = librosa.frames_to_time(np.arange(len(f0)), sr=sr)
    
    return f0_filtered, voiced_flag, voiced_probs, times, sr

def create_midi_with_timing(f0, voiced_flag, voiced_probs, times, confidence_threshold=0.6):
    # Create a PrettyMIDI object
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano
    
    # Process pitch track into notes with proper timing
    current_note = None
    note_start_time = None
    min_note_duration = 0.1  # Minimum note duration in seconds
    
    for i, (pitch, is_voiced, confidence, time) in enumerate(zip(f0, voiced_flag, voiced_probs, times)):
        # Check if we have a confident pitch
        if is_voiced and confidence > confidence_threshold and not np.isnan(pitch):
            midi_note = int(round(librosa.hz_to_midi(pitch)))
            
            # If this is a new note or continuation of current note
            if current_note is None:
                # Start new note
                current_note = midi_note
                note_start_time = time
            elif abs(midi_note - current_note) > 0.5:  # Note changed
                # End previous note if it's long enough
                if note_start_time is not None and (time - note_start_time) >= min_note_duration:
                    note = pretty_midi.Note(
                        velocity=100,
                        pitch=current_note,
                        start=note_start_time,
                        end=time
                    )
                    instrument.notes.append(note)
                
                # Start new note
                current_note = midi_note
                note_start_time = time
        else:
            # No pitch detected, end current note if exists
            if current_note is not None and note_start_time is not None:
                if (time - note_start_time) >= min_note_duration:
                    note = pretty_midi.Note(
                        velocity=100,
                        pitch=current_note,
                        start=note_start_time,
                        end=time
                    )
                    instrument.notes.append(note)
                current_note = None
                note_start_time = None
    
    # Handle final note
    if current_note is not None and note_start_time is not None:
        final_time = times[-1] if len(times) > 0 else note_start_time + min_note_duration
        if (final_time - note_start_time) >= min_note_duration:
            note = pretty_midi.Note(
                velocity=100,
                pitch=current_note,
                start=note_start_time,
                end=final_time
            )
            instrument.notes.append(note)
    
    midi.instruments.append(instrument)
    return midi

def visualize_results(f0, voiced_flag, times, midi_object):
    """Optional: visualize the pitch tracking and resulting MIDI"""
    plt.figure(figsize=(12, 8))
    
    # Plot 1: Pitch track
    plt.subplot(2, 1, 1)
    plt.plot(times, f0, 'b-', alpha=0.7, label='Detected Pitch (Hz)')
    plt.plot(times[voiced_flag], f0[voiced_flag], 'ro', markersize=2, label='Voiced segments')
    plt.ylabel('Frequency (Hz)')
    plt.title('Pitch Tracking Results')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: MIDI notes
    plt.subplot(2, 1, 2)
    for note in midi_object.instruments[0].notes:
        plt.plot([note.start, note.end], [note.pitch, note.pitch], 'g-', linewidth=3)
        plt.plot(note.start, note.pitch, 'go', markersize=5)
    
    plt.ylabel('MIDI Note Number')
    plt.xlabel('Time (seconds)')
    plt.title('Generated MIDI Notes')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Main execution
if __name__ == "__main__":
    audio_path = "new_music.mp3"
    
    try:
        # Extract melody with improved method
        f0, voiced_flag, voiced_probs, times, sr = extract_melody_improved(audio_path)
        
        # Create MIDI with proper timing
        midi = create_midi_with_timing(f0, voiced_flag, voiced_probs, times)
        
        # Save MIDI file
        midi_path = "whistle_converted_melody_improved.mid"
        midi.write(midi_path)
        
        print(f"MIDI file created: {midi_path}")
        print(f"Number of notes generated: {len(midi.instruments[0].notes)}")
        
        # Optional: visualize results
        # visualize_results(f0, voiced_flag, times, midi)
        
    except Exception as e:
        print(f"Error processing audio: {e}")
        print("Make sure the audio file exists and is in a supported format.")