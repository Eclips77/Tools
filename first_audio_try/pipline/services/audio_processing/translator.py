from pathlib import Path
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

class Translator:
    """
    A class to translate text in default from English to Hebrew using a pre-trained model.
    """
    def __init__(self, model_name="Helsinki-NLP/opus-mt-en-he"):
        """
        Initializes the Translator by loading the translation model and tokenizer.
        Args:
            model_name (str): The name of the pre-trained model to use.
        """
        self.translator = self._load_translator(model_name)

    def _load_translator(self, model_name: str,input_language="en", target_language="he"):
        """
        Loads the translation model and tokenizer.
        Args:
            model_name (str): The name of the pre-trained model.
        Returns:
            A translation pipeline.
        """
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        return pipeline("translation", model=model, tokenizer=tokenizer, src_lang=input_language, tgt_lang=target_language, max_length=512)

    def translate_line(self, line: str) -> str:
        """
        Translates a single line of text, preserving timestamps if present.
        Args:
            line (str): The line of text to translate.
        Returns:
            The translated line.
        """
        line = line.strip()
        if not line:
            return ""

        match = re.match(r"^\[(.+?)\s*->\s*(.+?)\]\s*(.*)$", line)
        if not match:
            return self.translator(line)[0]["translation_text"]

        start, end, text = match.groups()
        if not text.strip():
            return f"[{start} -> {end}]"

        translated_text = self.translator(text)[0]["translation_text"]
        return f"[{start} -> {end}] {translated_text}"

    def translate_file(self, src_path: Path, dst_path: Path) -> None:
        """
        Translates a text file line by line from English to Hebrew.
        Args:
            src_path (Path): The path to the source text file.
            dst_path (Path): The path to the destination text file.
        """
        if not src_path.exists():
            raise FileNotFoundError(f"Missing source file: {src_path}")

        with src_path.open("r", encoding="utf-8") as fin, dst_path.open("w", encoding="utf-8") as fout:
            for line in fin:
                translated_line = self.translate_line(line)
                fout.write(translated_line + "\n")


def main():
    """
    Main function to run the translation process on default files.
    """
    # Adjust the path to point to the root of the project where the files are
    base_dir = Path(__file__).resolve().parent.parent.parent
    src = base_dir / "transcript_en.txt"
    dst = base_dir / "transcript_he.txt"

    translator = Translator()
    translator.translate_file(src, dst)
    print(f"Translation complete. Output written to {dst}")

if __name__ == "__main__":
    main()
