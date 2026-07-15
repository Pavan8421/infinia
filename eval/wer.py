"""Round-trip WER: generated WAV → ASR → compare to input text. Target ≤ 10%."""

from __future__ import annotations

from pathlib import Path
from typing import Optional


def normalize_text(text: str) -> str:
    """Light normalization before WER (lowercase, strip punctuation). Extend per language."""
    import re

    t = text.strip().lower()
    t = re.sub(r"[^\w\s\u0600-\u06FF\u0900-\u097F\u0C00-\u0C7F]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t


def compute_wer(reference: str, hypothesis: str) -> float:
    """
    Word error rate as a percentage.

    Requires `jiwer` (see requirements/eval.txt). Raises if not installed.
    """
    try:
        from jiwer import wer
    except ImportError as e:
        raise ImportError("Install jiwer: pip install -r requirements/eval.txt") from e
    return 100.0 * float(wer(normalize_text(reference), normalize_text(hypothesis)))


def transcribe(wav_path: str | Path, language: Optional[str] = None) -> str:
    """
    ASR transcription. Phase 3: Whisper large-v3 / IndicWhisper.

    language: ISO-ish hint — en, ar, hi, te
    """
    raise NotImplementedError(
        f"transcribe({wav_path!s}, language={language!r}): wire Whisper in Phase 3"
    )


def round_trip_wer(
    wav_path: str | Path,
    reference_text: str,
    language: Optional[str] = None,
) -> dict:
    """Return {'wer_pct': float, 'hypothesis': str, 'reference': str}."""
    hyp = transcribe(wav_path, language=language)
    return {
        "wer_pct": compute_wer(reference_text, hyp),
        "hypothesis": hyp,
        "reference": reference_text,
        "wav_path": str(wav_path),
        "language": language,
    }
