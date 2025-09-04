"""
File Manager Module

This module provides utilities for managing transcription files,
including saving, loading, and batch processing.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import glob

from .recognition_result import TranscriptionResult


class TranscriptionFileManager:
    """
    Class for managing transcription files.
    
    This class provides methods for saving, loading, and organizing
    transcription results in various formats.
    """
    
    def __init__(self, output_dir: Optional[str] = None) -> None:
        """
        Initialize the transcription file manager.
        
        Args:
            output_dir: Default directory for output files. Defaults to None.
        """
        self.output_dir = output_dir
    
    def save_transcription(self, result: TranscriptionResult, output_path: str, 
                          format_type: str = "auto") -> str:
        """
        Save a transcription result to a file.
        
        Args:
            result: The transcription result.
            output_path: Path where to save the transcription.
            format_type: Format to save in ('auto', 'json', 'txt', 'srt', 'vtt').
                       Defaults to "auto" (detect from extension).
            
        Returns:
            str: Path to the saved file.
            
        Raises:
            ValueError: If format is unsupported.
        """
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Determine format type if auto
        if format_type == "auto":
            _, ext = os.path.splitext(output_path)
            format_type = ext.lower().lstrip('.')
            
            # Default to txt if unknown extension
            if format_type not in ['json', 'txt', 'srt', 'vtt']:
                format_type = 'txt'
        
        # Save in the appropriate format
        if format_type == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
                
        elif format_type == 'txt':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.text)
                
        elif format_type == 'srt':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.to_srt())
                
        elif format_type == 'vtt':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.to_vtt())
                
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
            
        return output_path
    
    def load_transcription(self, file_path: str) -> TranscriptionResult:
        """
        Load a transcription from a file.
        
        Args:
            file_path: Path to the transcription file.
            
        Returns:
            TranscriptionResult: The loaded transcription.
            
        Raises:
            ValueError: If the file format is unsupported.
        """
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return TranscriptionResult.from_dict(data)
                
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                return TranscriptionResult(text=text)
                
        else:
            raise ValueError(f"Unsupported file format for loading: {ext}")
    
    def save_batch_transcriptions(self, results: Dict[str, TranscriptionResult], 
                                 output_dir: Optional[str] = None,
                                 format_type: str = "txt") -> Dict[str, str]:
        """
        Save multiple transcription results.
        
        Args:
            results: Dictionary mapping identifiers to transcription results.
            output_dir: Directory to save the files in. Defaults to None (use self.output_dir).
            format_type: Format to save in. Defaults to "txt".
            
        Returns:
            Dict[str, str]: Dictionary mapping identifiers to saved file paths.
            
        Raises:
            ValueError: If output_dir is not specified and self.output_dir is None.
        """
        if output_dir is None:
            output_dir = self.output_dir
            
        if output_dir is None:
            raise ValueError("No output directory specified")
            
        os.makedirs(output_dir, exist_ok=True)
        
        saved_paths = {}
        
        for identifier, result in results.items():
            # Create a sanitized filename
            safe_id = "".join([c if c.isalnum() else "_" for c in identifier])
            file_path = os.path.join(output_dir, f"{safe_id}.{format_type}")
            
            saved_path = self.save_transcription(result, file_path, format_type)
            saved_paths[identifier] = saved_path
            
        return saved_paths
    
    def create_merged_transcription(self, results: List[TranscriptionResult], 
                                  output_path: Optional[str] = None) -> TranscriptionResult:
        """
        Merge multiple transcription results into a single result.
        
        Args:
            results: List of transcription results to merge.
            output_path: Path to save the merged result. Defaults to None (don't save).
            
        Returns:
            TranscriptionResult: Merged transcription result.
        """
        if not results:
            return TranscriptionResult(text="")
            
        # Concatenate all texts with newline separators
        merged_text = "\n\n".join(result.text for result in results)
        
        # Merge segments, adjusting timestamps if needed
        merged_segments = []
        time_offset = 0.0
        
        for result in results:
            segments = result.segments.copy() if result.segments else []
            
            # If this isn't the first result and we have segments, add time offset
            if merged_segments and segments:
                # Find the last end time from previous segments
                last_end = merged_segments[-1]['end']
                
                # Calculate new offset
                time_offset = last_end + 1.0  # 1 second gap between merged parts
                
                # Adjust timestamps
                for segment in segments:
                    segment['start'] += time_offset
                    segment['end'] += time_offset
            
            # Add the adjusted segments
            merged_segments.extend(segments)
        
        # Create merged result
        merged_result = TranscriptionResult(
            text=merged_text,
            segments=merged_segments,
            language=results[0].language if results else None,
            source="merged",
            metadata={"source_count": len(results)}
        )
        
        # Save if output_path specified
        if output_path:
            self.save_transcription(merged_result, output_path)
            
        return merged_result
    
    def find_transcriptions(self, directory: Optional[str] = None, 
                          file_pattern: str = "*.json") -> Dict[str, str]:
        """
        Find transcription files in a directory.
        
        Args:
            directory: Directory to search in. Defaults to None (use self.output_dir).
            file_pattern: Glob pattern for files. Defaults to "*.json".
            
        Returns:
            Dict[str, str]: Dictionary mapping base filenames to full paths.
            
        Raises:
            ValueError: If directory is not specified and self.output_dir is None.
        """
        if directory is None:
            directory = self.output_dir
            
        if directory is None:
            raise ValueError("No directory specified")
            
        files = {}
        
        for file_path in glob.glob(os.path.join(directory, file_pattern)):
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            files[base_name] = file_path
            
        return files
    
    def load_multiple_transcriptions(self, file_paths: List[str]) -> Dict[str, TranscriptionResult]:
        """
        Load multiple transcription files.
        
        Args:
            file_paths: List of file paths to load.
            
        Returns:
            Dict[str, TranscriptionResult]: Dictionary mapping base filenames to results.
        """
        results = {}
        
        for file_path in file_paths:
            try:
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                results[base_name] = self.load_transcription(file_path)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                
        return results
