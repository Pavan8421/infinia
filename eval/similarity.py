"""Speaker similarity: embed reference + generated → cosine. Target ≥ 0.75."""

from __future__ import annotations

from pathlib import Path

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=np.float64).reshape(-1)
    b = np.asarray(b, dtype=np.float64).reshape(-1)
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def embed_speaker(wav_path: str | Path) -> np.ndarray:
    """
    Speaker embedding via Resemblyzer (or SpeechBrain ECAPA).

    Phase 3: implement with requirements/eval.txt.
    """
    raise NotImplementedError(
        f"embed_speaker({wav_path!s}): wire Resemblyzer / ECAPA in Phase 3"
    )


def speaker_similarity(
    reference_wav: str | Path,
    generated_wav: str | Path,
) -> dict:
    """Return {'cosine': float, 'reference': str, 'generated': str}."""
    ref_emb = embed_speaker(reference_wav)
    gen_emb = embed_speaker(generated_wav)
    return {
        "cosine": cosine_similarity(ref_emb, gen_emb),
        "reference": str(reference_wav),
        "generated": str(generated_wav),
    }
