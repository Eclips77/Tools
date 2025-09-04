from pathlib import Path
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

def load_translator():
    """
    Load the English to Hebrew translation model and tokenizer.
        Returns a translation pipeline.
    """
    model_name = "Helsinki-NLP/opus-mt-en-he"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return pipeline("translation", model=model, tokenizer=tokenizer, src_lang="en", tgt_lang="he", max_length=512)

def translate_line(translator, line: str) -> str:
    """
    Translate a line of text, preserving timestamps if present.
        Arguments:
            translator: The translation pipeline.
            line: The line of text to translate.  
       Returns the translated line.
    """
    m = re.match(r"^\[(.+?)\s*->\s*(.+?)\]\s*(.*)$", line.strip())
    if not m:
        if not line.strip():
            return ""
        out = translator(line.strip())[0]["translation_text"]
        return out
    start, end, text = m.group(1), m.group(2), m.group(3)
    if not text.strip():
        return f"[{start} -> {end}]"
    out = translator(text)[0]["translation_text"]
    return f"[{start} -> {end}] {out}"

def main():
    """
    Translate the transcript from English to Hebrew.
    """
    base_dir = Path(__file__).parent
    src = base_dir / "transcript_en.txt"
    dst = base_dir / "transcript_he.txt"

    if not src.exists():
        raise FileNotFoundError(f"Missing source file: {src}")

    translator = load_translator()

    with src.open("r", encoding="utf-8") as fin, dst.open("w", encoding="utf-8") as fout:
        for line in fin:
            he = translate_line(translator, line)
            fout.write(he + ("\n" if not he.endswith("\n") else ""))

if __name__ == "__main__":
    main()
