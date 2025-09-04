from pathlib import Path
from faster_whisper import WhisperModel

def main():
    audio_path = Path(__file__).parent / "audio_data" / "boby_podcast.mp3"
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio not found: {audio_path}")

    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(audio_path), task="transcribe", beam_size=5, vad_filter=True)

    print("Detected language:", info.language)
    out_path = Path(__file__).parent / "transcript_en.txt"
    with out_path.open("w", encoding="utf-8") as f:
        for s in segments:
            line = f"[{s.start:.2f}s -> {s.end:.2f}s] {s.text}\n"
            print(line, end="")
            f.write(line)

if __name__ == "__main__":
    main()
