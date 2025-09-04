"""
Recognition Result Module

This module provides classes for representing and working with
speech recognition and transcription results.
"""

from typing import Dict, List, Optional, Any, Union
import json
from datetime import timedelta


class TranscriptionResult:
    """
    Class representing the result of a transcription operation.
    
    This class provides a unified interface for working with transcription results
    from various sources, with methods for converting to different formats.
    
    Attributes:
        text (str): The full transcribed text.
        segments (List[Dict]): List of segments with timing information.
        language (Optional[str]): Detected or specified language.
        source (str): Source of the transcription (e.g., 'whisper', 'google_speech').
        metadata (Dict[str, Any]): Additional metadata about the transcription.
    """
    
    def __init__(self, text: str, segments: Optional[List[Dict[str, Any]]] = None, 
                language: Optional[str] = None, source: str = "unknown", 
                metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize a transcription result.
        
        Args:
            text: The full transcribed text.
            segments: List of segments with timing information. Defaults to None.
            language: Detected or specified language. Defaults to None.
            source: Source of the transcription. Defaults to "unknown".
            metadata: Additional metadata. Defaults to None.
        """
        self.text = text
        self.segments = segments or []
        self.language = language
        self.source = source
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the result to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the result.
        """
        return {
            'text': self.text,
            'segments': self.segments,
            'language': self.language,
            'source': self.source,
            'metadata': self.metadata
        }
    
    def to_json(self, indent: int = 2) -> str:
        """
        Convert the result to a JSON string.
        
        Args:
            indent: JSON indentation. Defaults to 2.
            
        Returns:
            str: JSON string representation.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
    
    def _format_timestamp(self, seconds: float) -> str:
        """
        Format seconds as HH:MM:SS,mmm for SRT or WebVTT.
        
        Args:
            seconds: Timestamp in seconds.
            
        Returns:
            str: Formatted timestamp.
        """
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = round(td.microseconds / 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
    
    def to_srt(self) -> str:
        """
        Convert the result to SubRip (SRT) format.
        
        Returns:
            str: SRT format subtitles.
        """
        if not self.segments:
            return ""
            
        lines = []
        for i, segment in enumerate(self.segments, 1):
            start = self._format_timestamp(segment['start'])
            end = self._format_timestamp(segment['end'])
            
            lines.append(f"{i}")
            lines.append(f"{start} --> {end}")
            lines.append(f"{segment['text']}")
            lines.append("")  # Empty line between entries
            
        return "\n".join(lines)
    
    def to_vtt(self) -> str:
        """
        Convert the result to WebVTT format.
        
        Returns:
            str: WebVTT format subtitles.
        """
        if not self.segments:
            return "WEBVTT\n\n"
            
        lines = ["WEBVTT", ""]  # Header and blank line
        
        for i, segment in enumerate(self.segments):
            # WebVTT uses . instead of , for milliseconds
            start = self._format_timestamp(segment['start']).replace(',', '.')
            end = self._format_timestamp(segment['end']).replace(',', '.')
            
            lines.append(f"{i + 1}")
            lines.append(f"{start} --> {end}")
            lines.append(f"{segment['text']}")
            lines.append("")  # Empty line between entries
            
        return "\n".join(lines)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TranscriptionResult':
        """
        Create a TranscriptionResult from a dictionary.
        
        Args:
            data: Dictionary with transcription data.
            
        Returns:
            TranscriptionResult: New instance.
        """
        return cls(
            text=data['text'],
            segments=data.get('segments', []),
            language=data.get('language'),
            source=data.get('source', 'unknown'),
            metadata=data.get('metadata', {})
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'TranscriptionResult':
        """
        Create a TranscriptionResult from a JSON string.
        
        Args:
            json_str: JSON string with transcription data.
            
        Returns:
            TranscriptionResult: New instance.
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def get_word_count(self) -> int:
        """
        Count the number of words in the transcription.
        
        Returns:
            int: Number of words.
        """
        return len(self.text.split())
    
    def get_duration(self) -> Optional[float]:
        """
        Get the total duration of the transcription in seconds.
        
        Returns:
            Optional[float]: Duration in seconds, or None if no segments.
        """
        if not self.segments:
            return None
            
        return max(segment['end'] for segment in self.segments)
