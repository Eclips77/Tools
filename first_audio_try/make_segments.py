import re, json
from pathlib import Path
from datetime import datetime

def parse_lines(path):
    lines = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^\[(.+?)\s*->\s*(.+?)\]\s*(.*)$", line.strip())
            if m:
                start, end, text = m.group(1), m.group(2), m.group(3)
                lines.append((float(start[:-1]) if start.endswith("s") else float(start),
                              float(end[:-1]) if end.endswith("s") else float(end),
                              text))
    return lines

def main():
    base = Path(__file__).parent
    en_path = base / "transcript_en.txt"
    he_path = base / "transcript_he.txt"

    en_segments = parse_lines(en_path)
    he_segments = parse_lines(he_path)

    audio_id = "boby_podcast"
    now = datetime.utcnow().isoformat() + "Z"

    records = []
    for (s_en, e_en, t_en), (_, _, t_he) in zip(en_segments, he_segments):
        records.append({
            "audio_id": audio_id,
            "lang_src": "en",
            "lang_tgt": "he",
            "start": s_en,
            "end": e_en,
            "text_en": t_en,
            "text_he": t_he,
            "created_at": now
        })

    out_path = base / f"{audio_id}_segments.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
