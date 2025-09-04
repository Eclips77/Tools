"""
Audio Transcription Module

This module provides abstract and concrete implementations for audio transcription
using various speech recognition libraries.
"""

import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union, BinaryIO
import json
from pathlib import Path

from .recognition_result import TranscriptionResult


class BaseTranscriber(ABC):
    """
    Abstract base class for audio transcription services.
    
    This class defines the common interface for all transcribers,
    regardless of the underlying library or service being used.
    """
    
    @abstractmethod
    def transcribe_file(self, audio_file_path: str) -> TranscriptionResult:
        """
        Transcribe audio from a file.
        
        Args:
            audio_file_path: Path to the audio file.
            
        Returns:
            TranscriptionResult: The transcription result.
        """
        pass
    
    @abstractmethod
    def transcribe_stream(self, audio_stream: BinaryIO) -> TranscriptionResult:
        """
        Transcribe audio from a binary stream.
        
        Args:
            audio_stream: Binary stream of audio data.
            
        Returns:
            TranscriptionResult: The transcription result.
        """
        pass
    
    def save_transcription(self, result: TranscriptionResult, output_path: str) -> str:
        """
        Save transcription result to a file.
        
        Args:
            result: The transcription result.
            output_path: Path where to save the transcription.
            
        Returns:
            str: Path to the saved file.
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Determine file format based on extension
        _, ext = os.path.splitext(output_path)
        ext = ext.lower()
        
        if ext == '.json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
        elif ext == '.txt':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.text)
        elif ext == '.srt':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.to_srt())
        elif ext == '.vtt':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.to_vtt())
        else:
            # Default to txt
            output_path = output_path + '.txt'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.text)
                
        return output_path


class WhisperTranscriber(BaseTranscriber):
    """
    Transcriber that uses OpenAI's Whisper model.
    
    This class provides methods for transcribing audio using the Whisper model,
    which can run locally for privacy and offline usage.
    """
    
    def __init__(self, model_name: str = "base", language: Optional[str] = None, 
                device: Optional[str] = None) -> None:
        """
        Initialize the Whisper transcriber.
        
        Args:
            model_name: Whisper model name ('tiny', 'base', 'small', 'medium', 'large').
                      Defaults to "base".
            language: Language code (e.g., 'en', 'he'). Defaults to None (auto-detect).
            device: Device to use ('cpu', 'cuda', etc.). Defaults to None (auto-select).
        """
        try:
            import whisper
        except ImportError:
            raise ImportError(
                "Whisper is required for WhisperTranscriber. "
                "Install it with: pip install openai-whisper"
            )
            
        self.model_name = model_name
        self.language = language
        self.device = device
        self.model = whisper.load_model(model_name, device=device)
    
    def transcribe_file(self, audio_file_path: str) -> TranscriptionResult:
        """
        Transcribe audio from a file using Whisper.
        
        Args:
            audio_file_path: Path to the audio file.
            
        Returns:
            TranscriptionResult: The transcription result.
        """
        result = self.model.transcribe(
            audio_file_path, 
            language=self.language,
            verbose=False
        )
        
        segments = []
        for segment in result.get('segments', []):
            segments.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'].strip()
            })
        
        return TranscriptionResult(
            text=result['text'],
            segments=segments,
            language=result.get('language', self.language),
            source='whisper',
            metadata={'model': self.model_name}
        )
    
    def transcribe_stream(self, audio_stream: BinaryIO) -> TranscriptionResult:
        """
        Transcribe audio from a stream using Whisper.
        
        Args:
            audio_stream: Binary stream of audio data.
            
        Returns:
            TranscriptionResult: The transcription result.
        """
        # Save stream to a temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file_path = temp_file.name
            audio_stream.seek(0)
            temp_file.write(audio_stream.read())
            
        try:
            # Transcribe the temporary file
            return self.transcribe_file(temp_file_path)
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)


class GoogleSpeechTranscriber(BaseTranscriber):
    """
    Transcriber that uses Google Speech-to-Text API.
    
    This class provides methods for transcribing audio using Google's cloud service.
    """
    
    def __init__(self, language_code: str = "en-US", credentials_path: Optional[str] = None, 
                 enable_punctuation: bool = True) -> None:
        """
        Initialize the Google Speech transcriber.
        
        Args:
            language_code: Language code (e.g., 'en-US', 'he-IL'). Defaults to "en-US".
            credentials_path: Path to Google API credentials JSON file. Defaults to None.
            enable_punctuation: Whether to enable automatic punctuation. Defaults to True.
        """
        try:
            from google.cloud import speech
        except ImportError:
            raise ImportError(
                "Google Cloud Speech is required. "
                "Install it with: pip install google-cloud-speech"
            )
            
        self.language_code = language_code
        self.enable_punctuation = enable_punctuation
        
        # Set credentials if provided
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            
        self.client = speech.SpeechClient()
    
    def transcribe_file(self, audio_file_path: str) -> TranscriptionResult:
        """
        Transcribe audio from a file using Google Speech API.
        
        Args:
            audio_file_path: Path to the audio file.
            
        Returns:
            TranscriptionResult: The transcription result.
        """
        from google.cloud import speech
        
        with open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()
            
        audio = speech.RecognitionAudio(content=content)
        
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code=self.language_code,
            enable_automatic_punctuation=self.enable_punctuation,
            enable_word_time_offsets=True
        )
        
        response = self.client.recognize(config=config, audio=audio)
        
        # Process response
        full_text = ""
        segments = []
        
        for result in response.results:
            transcript = result.alternatives[0].transcript
            full_text += transcript + " "
            
            if result.alternatives[0].words:
                start_time = result.alternatives[0].words[0].start_time.total_seconds()
                end_time = result.alternatives[0].words[-1].end_time.total_seconds()
                
                segments.append({
                    'start': start_time,
                    'end': end_time,
                    'text': transcript.strip()
                })
        
        return TranscriptionResult(
            text=full_text.strip(),
            segments=segments,
            language=self.language_code,
            source='google_speech',
            metadata={'enable_punctuation': self.enable_punctuation}
        )
    
    def transcribe_stream(self, audio_stream: BinaryIO) -> TranscriptionResult:
        """
        Transcribe audio from a stream using Google Speech API.
        
        Args:
            audio_stream: Binary stream of audio data.
            
        Returns:
            TranscriptionResult: The transcription result.
        """
        # Save stream to a temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file_path = temp_file.name
            audio_stream.seek(0)
            temp_file.write(audio_stream.read())
            
        try:
            # Transcribe the temporary file
            return self.transcribe_file(temp_file_path)
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)


class TranscriberFactory:
    """
    Factory class for creating transcriber instances.
    
    This class provides methods to create different transcriber instances
    based on the specified engine.
    """
    
    @staticmethod
    def create(engine: str = 'whisper', **kwargs: Any) -> BaseTranscriber:
        """
        Create a transcriber instance.
        
        Args:
            engine: Transcription engine to use ('whisper', 'google'). Defaults to 'whisper'.
            **kwargs: Additional arguments to pass to the transcriber constructor.
            
        Returns:
            BaseTranscriber: A transcriber instance.
            
        Raises:
            ValueError: If the specified engine is not supported.
        """
        engine = engine.lower()
        
        if engine == 'whisper':
            return WhisperTranscriber(**kwargs)
        elif engine == 'google':
            return GoogleSpeechTranscriber(**kwargs)
        else:
            raise ValueError(f"Unsupported transcription engine: {engine}")
