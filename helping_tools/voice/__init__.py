"""
Voice Processing and Transcription Package

This package provides utilities for processing audio and transcribing speech to text
using various speech recognition engines and tools.
"""

from .recognition_result import TranscriptionResult
from .transcriber import (
    BaseTranscriber,
    WhisperTranscriber,
    GoogleSpeechTranscriber,
    TranscriberFactory
)
from .audio_processor import AudioProcessor
from .file_manager import TranscriptionFileManager

__all__ = [
    'TranscriptionResult',
    'BaseTranscriber',
    'WhisperTranscriber',
    'GoogleSpeechTranscriber',
    'TranscriberFactory',
    'AudioProcessor',
    'TranscriptionFileManager',
]
