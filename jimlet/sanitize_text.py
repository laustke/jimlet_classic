
import re
import unicodedata

SAFE_CHARS_RE = re.compile(
    r"[^a-zA-Z0-9\s\.\,\!\?\:\;\'\"\-\(\)]"
)

SYMBOL_REPLACEMENTS = {
    "&": " and ",
    "%": " percent ",
    "@": " at ",
    "#": " number ",
}

def sanitize_text(text: str) -> str:





    text = unicodedata.normalize("NFKC", text)

    text = text.replace("—", " ")
    text = text.replace("–", " ")

    text = text.translate(str.maketrans({
        "[": " ",
        "]": " ",
        "{": " ",
        "}": " ",
        "<": " ",
        ">": " ",
    }))

    for symbol, replacement in SYMBOL_REPLACEMENTS.items():
        text = text.replace(symbol, replacement)

    text = SAFE_CHARS_RE.sub("", text)

    text = re.sub(r"[!?]{2,}", ".", text)
    text = re.sub(r"\.{3,}", ".", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()
