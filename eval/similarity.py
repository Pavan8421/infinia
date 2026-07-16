"""Speaker similarity: embed reference + generated → cosine. Target ≥ 0.75."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import numpy as np

_encoder: Any = None


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=np.float64).reshape(-1)
    b = np.asarray(b, dtype=np.float64).reshape(-1)
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def get_voice_encoder(device: Optional[str] = None):
    """Lazy-load Resemblyzer VoiceEncoder (cached)."""
    global _encoder
    if _encoder is not None:
        return _encoder
    try:
        import torch
        from resemblyzer import VoiceEncoder
    except ImportError as e:
        raise ImportError(
            "Install resemblyzer (+ setuptools<81 for webrtcvad): "
            "pip install -r requirements/eval.txt"
        ) from e

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    # Resemblyzer accepts device as string "cpu"/"cuda"
    _encoder = VoiceEncoder(device=device)
    return _encoder


def embed_speaker(
    wav_path: str | Path,
    *,
    device: Optional[str] = None,
) -> np.ndarray:
    """
    Speaker embedding via Resemblyzer.

    Returns a 256-D L2-oriented embedding (float32).
    """
    from resemblyzer import preprocess_wav

    path = Path(wav_path)
    if not path.is_file():
        raise FileNotFoundError(f"Audio not found: {path}")

    wav = preprocess_wav(path)
    encoder = get_voice_encoder(device=device)
    emb = encoder.embed_utterance(wav)
    return np.asarray(emb, dtype=np.float32)


def speaker_similarity(
    reference_wav: str | Path,
    generated_wav: str | Path,
    *,
    device: Optional[str] = None,
) -> dict:
    """Return {'cosine': float, 'reference': str, 'generated': str, ...}."""
    ref_emb = embed_speaker(reference_wav, device=device)
    gen_emb = embed_speaker(generated_wav, device=device)
    cos = cosine_similarity(ref_emb, gen_emb)
    return {
        "cosine": cos,
        "meets_target": cos >= 0.75,
        "reference": str(reference_wav),
        "generated": str(generated_wav),
        "method": "resemblyzer",
    }
