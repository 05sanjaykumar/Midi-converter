# Whistle to MIDI Converter

A Python tool that converts whistled melodies from audio files into MIDI format using advanced pitch detection and audio processing techniques.

## Overview

This project takes an audio file containing a whistled melody and automatically converts it into a MIDI file that can be played back, edited in music software, or used for further musical analysis. The tool uses sophisticated pitch tracking algorithms to detect the fundamental frequency of the whistle and converts those pitches into properly timed MIDI notes.

## Features

- **Advanced Pitch Detection**: Uses librosa's pYIN algorithm optimized for monophonic sources
- **Intelligent Note Segmentation**: Automatically detects note onsets and offsets
- **Confidence-Based Filtering**: Only converts high-confidence pitch detections
- **Proper Timing**: Maintains realistic note durations based on the original audio
- **Noise Filtering**: Applies median filtering to smooth pitch tracks
- **Visualization Support**: Optional plotting of pitch detection results
- **Error Handling**: Robust error handling and user feedback

## Requirements

### Python Dependencies

```bash
pip install librosa
pip install pretty_midi
pip install numpy
pip install matplotlib
pip install scipy
pip install setuptools  # Required for pretty_midi compatibility
```

### System Requirements

- Python 3.8 or higher
- Audio codecs for your input format (MP3, WAV, FLAC, etc.)
- Sufficient RAM for audio processing (typically 1-2GB for most audio files)

## Installation

1. Clone or download this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

1. Place your whistled audio file in the project directory
2. Update the `audio_path` variable in the script with your filename
3. Run the script:
   ```bash
   python whistle_to_midi.py
   ```

### Input Requirements

For best results, your audio should have:
- **Clear whistling**: Avoid background noise or multiple sound sources
- **Monophonic melody**: Single notes, not chords
- **Good signal-to-noise ratio**: Clear, audible whistling
- **Appropriate pitch range**: Roughly C4 to C7 (middle C to high C)
- **Consistent volume**: Avoid very quiet or distorted sections

### Supported Audio Formats

- MP3
- WAV
- FLAC
- M4A
- And most formats supported by librosa/ffmpeg

## Configuration Options

### Pitch Detection Parameters

- `fmin`: Minimum frequency to detect (default: C4 ≈ 262 Hz)
- `fmax`: Maximum frequency to detect (default: C7 ≈ 2093 Hz)
- `confidence_threshold`: Minimum confidence for pitch detection (default: 0.6)

### Timing Parameters

- `min_note_duration`: Minimum note length in seconds (default: 0.1)
- `median_filter_size`: Smoothing kernel size (default: 5)

### Example Configuration

```python
# Adjust these parameters in the script for different results
f0, voiced_flag, voiced_probs = librosa.pyin(y, 
                                             fmin=librosa.note_to_hz('C3'),  # Lower range
                                             fmax=librosa.note_to_hz('C8'),  # Higher range
                                             sr=sr)

confidence_threshold = 0.7  # Stricter confidence
min_note_duration = 0.2     # Longer minimum notes
```

## Output

The script generates:
- **MIDI file**: `whistle_converted_melody_improved.mid`
- **Console output**: Number of notes detected and file location
- **Optional visualization**: Pitch tracking and MIDI note plots

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'pkg_resources'"**
```bash
pip install --upgrade setuptools
```

**Poor pitch detection results:**
- Check audio quality (clear whistling, minimal background noise)
- Adjust `confidence_threshold` (try 0.4-0.8)
- Modify frequency range (`fmin`/`fmax`) to match your vocal range

**No notes generated:**
- Lower `confidence_threshold` to 0.3-0.4
- Check if audio contains clear pitched content
- Verify audio file is loading correctly

**Too many short notes:**
- Increase `min_note_duration` to 0.2-0.5 seconds
- Increase median filter size for more smoothing

### Debug Mode

Uncomment the visualization line to see what the algorithm detected:
```python
visualize_results(f0, voiced_flag, times, midi)
```

## Technical Details

### Algorithm Overview

1. **Audio Loading**: Load audio file using librosa
2. **Pitch Detection**: Extract fundamental frequency using pYIN algorithm
3. **Confidence Filtering**: Remove low-confidence pitch estimates
4. **Smoothing**: Apply median filtering to reduce noise
5. **Note Segmentation**: Group consecutive similar pitches into notes
6. **MIDI Generation**: Convert pitch and timing data to MIDI format

### Why pYIN?

The pYIN (probabilistic YIN) algorithm is specifically designed for monophonic pitch tracking and provides:
- Better accuracy for singing/whistling than general-purpose methods
- Confidence estimates for each pitch detection
- Robust handling of noise and silence

## Limitations

- **Monophonic only**: Cannot handle multiple simultaneous pitches
- **Pitch range**: Limited to the configured frequency range
- **Audio quality dependent**: Poor audio quality affects results
- **No rhythm quantization**: Maintains original timing without musical quantization
- **Single instrument**: All notes assigned to piano (program 0)

## Future Improvements

- Add rhythm quantization options
- Support for different MIDI instruments
- Batch processing of multiple files
- GUI interface
- Real-time processing capabilities
- Chord detection for polyphonic audio

## License

This project is open source. Feel free to modify and distribute.

## Contributing

Contributions are welcome! Areas for improvement:
- Better pitch detection algorithms
- User interface development
- Additional audio preprocessing options
- Performance optimizations
- Documentation improvements