from pathlib import Path
from faster_whisper import WhisperModel
import json
import logging
from translator import Translator 

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioProcessor:
    """
    A generic class to process audio files using the Whisper model for transcription.
    """
    def __init__(self, model_size="small", device="cpu", compute_type="int8"):
        """
        Initializes the AudioProcessor with a Whisper model.
        Args:
            model_size (str): The size of the Whisper model (e.g., "tiny", "base", "small").
            device (str): The device to run the model on ("cpu" or "cuda").
            compute_type (str): The compute type for the model (e.g., "int8", "float16").
        """
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        logger.info(f"Whisper model loaded: {model_size} ({device}, {compute_type})")

    def transcribe_audio(self, audio_path: Path, task="transcribe", beam_size=5, vad_filter=True):
        """
        Transcribes an audio file.
        Args:
            audio_path (Path): The path to the audio file.
            task (str): The task for the model ("transcribe" or "translate").
            beam_size (int): The beam size for decoding.
            vad_filter (bool): Whether to use the VAD filter.
        Returns:
            A tuple containing the list of segments and transcription info.
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"Transcribing {audio_path}...")
        segments, info = self.model.transcribe(
            str(audio_path),
            task=task,
            beam_size=beam_size,
            vad_filter=vad_filter
        )
        print(f"Detected language '{info.language}' with probability {info.language_probability:.2f}")
        # The segments generator needs to be converted to a list to be reused.
        return list(segments), info

    def save_as_text(self, segments, output_path: Path):
        """
        Saves the transcription segments as a text file with timestamps.
        Args:
            segments (list): A list of transcription segments.
            output_path (Path): The path to the output text file.
        """
        logger.info(f"Saving transcript to {output_path}...")
        with output_path.open("w", encoding="utf-8") as f:
            for s in segments:
                line = f"[{s.start:.2f}s -> {s.end:.2f}s] {s.text.strip()}\n"
                f.write(line)
        logger.info("Save complete.")

    def save_as_json(self, segments, output_path: Path):
        """
        Saves the transcription segments as a JSON file.
        Args:
            segments (list): A list of transcription segments.
            output_path (Path): The path to the output JSON file.
        """
        logger.info(f"Saving segments to {output_path}...")
        segment_data = [
            {"start": s.start, "end": s.end, "text": s.text.strip()}
            for s in segments
        ]
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(segment_data, f, indent=2, ensure_ascii=False)
        logger.info("Save complete.")


def main():
    """
    Main function to demonstrate the AudioProcessor class and the translation process.
    """
    # The script is in pipline/services/audio_processing, so we go up three levels to the project root.
    project_root = Path(__file__).resolve().parent.parent.parent
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True) # Create the output directory if it doesn't exist

    audio_path = project_root / "audio_data" / "boby_podcast.mp3"
    transcript_txt_path = output_dir / "transcript_en.txt"
    transcript_json_path = output_dir / "boby_podcast_segments.json"
    translated_txt_path = output_dir / "transcript_he.txt"


    try:
        # Step 1: Transcribe the audio
        processor = AudioProcessor(model_size="small")
        segments, info = processor.transcribe_audio(audio_path)

        # Step 2: Save the transcription output
        processor.save_as_text(segments, transcript_txt_path)
        processor.save_as_json(segments, transcript_json_path)
        logger.info("Transcription finished successfully!")

        # Step 3: Translate the transcribed text
        logger.info("Starting translation...")
        translator = Translator()
        translator.translate_file(transcript_txt_path, translated_txt_path)
        logger.info(f"Translation complete. Output written to {translated_txt_path}")

    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
