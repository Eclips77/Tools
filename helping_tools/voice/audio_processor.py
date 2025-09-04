"""
Audio Processor Module

This module provides classes for processing audio files before transcription,
such as format conversion, trimming, and noise reduction.
"""

import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union, BinaryIO, Tuple
from pathlib import Path
import tempfile


class AudioProcessor:
    """
    Class for processing audio files.
    
    This class provides methods for common audio processing tasks
    like format conversion, trimming, and noise reduction.
    """
    
    def __init__(self) -> None:
        """Initialize the audio processor."""
        try:
            import librosa
            import soundfile
        except ImportError:
            raise ImportError(
                "Required audio processing libraries are missing. "
                "Install them with: pip install librosa soundfile"
            )
    
    def convert_format(self, audio_path: str, output_format: str = "wav", 
                      output_path: Optional[str] = None) -> str:
        """
        Convert an audio file to a different format.
        
        Args:
            audio_path: Path to the input audio file.
            output_format: Target format (wav, mp3, flac, etc.). Defaults to "wav".
            output_path: Path for the output file. Defaults to None (auto-generate).
            
        Returns:
            str: Path to the converted file.
        """
        import librosa
        import soundfile as sf
        
        # Generate output path if not provided
        if output_path is None:
            base_path = os.path.splitext(audio_path)[0]
            output_path = f"{base_path}.{output_format}"
            
        # Load audio
        y, sr = librosa.load(audio_path, sr=None)
        
        # Save in new format
        sf.write(output_path, y, sr, format=output_format.upper())
        
        return output_path
    
    def trim_silence(self, audio_path: str, output_path: Optional[str] = None, 
                    top_db: int = 20) -> str:
        """
        Trim silence from the beginning and end of an audio file.
        
        Args:
            audio_path: Path to the input audio file.
            output_path: Path for the output file. Defaults to None (auto-generate).
            top_db: Threshold for silence detection in dB. Defaults to 20.
            
        Returns:
            str: Path to the trimmed file.
        """
        import librosa
        import soundfile as sf
        
        # Generate output path if not provided
        if output_path is None:
            base_path, ext = os.path.splitext(audio_path)
            output_path = f"{base_path}_trimmed{ext}"
            
        # Load audio
        y, sr = librosa.load(audio_path, sr=None)
        
        # Trim silence
        y_trimmed, trim_indices = librosa.effects.trim(y, top_db=top_db)
        
        # Save trimmed audio
        sf.write(output_path, y_trimmed, sr)
        
        return output_path
    
    def reduce_noise(self, audio_path: str, output_path: Optional[str] = None,
                    noise_reduce_amount: float = 0.5) -> str:
        """
        Reduce noise in an audio file.
        
        Args:
            audio_path: Path to the input audio file.
            output_path: Path for the output file. Defaults to None (auto-generate).
            noise_reduce_amount: Amount of noise reduction (0.0-1.0). Defaults to 0.5.
            
        Returns:
            str: Path to the noise-reduced file.
        """
        try:
            import noisereduce as nr
        except ImportError:
            raise ImportError(
                "Noisereduce library is required for noise reduction. "
                "Install it with: pip install noisereduce"
            )
            
        import librosa
        import soundfile as sf
        
        # Generate output path if not provided
        if output_path is None:
            base_path, ext = os.path.splitext(audio_path)
            output_path = f"{base_path}_denoised{ext}"
            
        # Load audio
        y, sr = librosa.load(audio_path, sr=None)
        
        # Reduce noise
        y_reduced = nr.reduce_noise(y=y, sr=sr, prop_decrease=noise_reduce_amount)
        
        # Save noise-reduced audio
        sf.write(output_path, y_reduced, sr)
        
        return output_path
    
    def split_audio(self, audio_path: str, output_dir: Optional[str] = None,
                  segment_length_sec: float = 60.0) -> List[str]:
        """
        Split an audio file into segments of specified length.
        
        Args:
            audio_path: Path to the input audio file.
            output_dir: Directory for output files. Defaults to None (same as input).
            segment_length_sec: Length of each segment in seconds. Defaults to 60.0.
            
        Returns:
            List[str]: List of paths to the segment files.
        """
        import librosa
        import soundfile as sf
        import numpy as np
        
        # Determine output directory
        if output_dir is None:
            output_dir = os.path.dirname(audio_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # Load audio
        y, sr = librosa.load(audio_path, sr=None)
        
        # Calculate segment length in samples
        segment_length_samples = int(segment_length_sec * sr)
        
        # Calculate number of segments
        num_segments = int(np.ceil(len(y) / segment_length_samples))
        
        # Get base filename
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        ext = os.path.splitext(audio_path)[1]
        
        segment_paths = []
        
        # Split and save segments
        for i in range(num_segments):
            start_sample = i * segment_length_samples
            end_sample = min((i + 1) * segment_length_samples, len(y))
            
            segment = y[start_sample:end_sample]
            
            segment_path = os.path.join(output_dir, f"{base_name}_segment_{i+1:03d}{ext}")
            sf.write(segment_path, segment, sr)
            
            segment_paths.append(segment_path)
            
        return segment_paths
    
    def extract_audio_from_video(self, video_path: str, output_path: Optional[str] = None) -> str:
        """
        Extract audio from a video file.
        
        Args:
            video_path: Path to the input video file.
            output_path: Path for the output audio file. Defaults to None (auto-generate).
            
        Returns:
            str: Path to the extracted audio file.
            
        Raises:
            RuntimeError: If FFmpeg is not available.
        """
        try:
            import subprocess
        except ImportError:
            raise ImportError(
                "Subprocess module is required for extracting audio from video."
            )
            
        # Check if FFmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=False)
        except FileNotFoundError:
            raise RuntimeError(
                "FFmpeg is required for extracting audio from video. "
                "Please install FFmpeg and make sure it's in your PATH."
            )
            
        # Generate output path if not provided
        if output_path is None:
            base_path = os.path.splitext(video_path)[0]
            output_path = f"{base_path}.wav"
            
        # Extract audio using FFmpeg
        subprocess.run([
            'ffmpeg',
            '-i', video_path,
            '-q:a', '0',
            '-map', 'a',
            output_path
        ], check=True)
        
        return output_path
    
    def get_audio_info(self, audio_path: str) -> Dict[str, Any]:
        """
        Get information about an audio file.
        
        Args:
            audio_path: Path to the audio file.
            
        Returns:
            Dict[str, Any]: Dictionary with audio information.
        """
        import librosa
        import numpy as np
        
        # Load audio file
        y, sr = librosa.load(audio_path, sr=None)
        
        # Calculate duration
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Get number of channels
        if len(y.shape) > 1:
            channels = y.shape[0]
        else:
            channels = 1
            
        # Calculate average volume (RMS)
        rms = np.sqrt(np.mean(y**2))
        
        return {
            'path': audio_path,
            'sample_rate': sr,
            'duration': duration,
            'channels': channels,
            'samples': len(y),
            'avg_volume': float(rms)
        }
