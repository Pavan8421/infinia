"""Round-trip WER: generated WAV → Whisper ASR → compare to input text. Target ≤ 10%."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

# Whisper model cache (lazy-loaded once per process)
_whisper_model: Any = None
_whisper_model_name: Optional[str] = None
_whisper_device: Optional[str] = None

# Map pipeline language labels → Whisper language codes
_LANG_TO_WHISPER = {
    "english": "en",
    "en": "en",
    "arabic": "ar",
    "ar": "ar",
    "hindi": "hi",
    "hi": "hi",
}


_ONES = {
    "zero": "0",
    "oh": "0",
    "o": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def spoken_digits_to_number(text: str) -> str:
    """Collapse runs of spoken digit words: 'two four seven' -> '247'."""
    words = text.split()
    out: list[str] = []
    buf: list[str] = []
    for w in words:
        if w in _ONES:
            buf.append(_ONES[w])
        else:
            if buf:
                out.append("".join(buf))
                buf = []
            out.append(w)
    if buf:
        out.append("".join(buf))
    return " ".join(out)


def normalize_text(text: str) -> str:
    """
    Normalize before WER: lowercase, strip punctuation, collapse spoken digits.

    Keeps Arabic / Devanagari letters. Maps 'two four seven' and '247'
    to the same token so ASR digit formatting does not inflate WER.
    """
    import re

    t = text.strip().lower()
    t = re.sub(r"[^\w\s\u0600-\u06FF\u0900-\u097F\u0C00-\u0C7F]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = spoken_digits_to_number(t)
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
    ref_n = normalize_text(reference)
    hyp_n = normalize_text(hypothesis)
    if not ref_n:
        return 0.0 if not hyp_n else 100.0
    return 100.0 * float(wer(ref_n, hyp_n))


def _resolve_model_name(model_name: Optional[str] = None) -> str:
    if model_name:
        return model_name
    try:
        from pipelines.config import load_config

        cfg = load_config()
        raw = cfg.get("eval", {}).get("asr", {}).get("default", "large-v3")
    except Exception:
        raw = "large-v3"
    # configs may use HuggingFace-style ids; openai-whisper wants short names
    aliases = {
        "openai/whisper-large-v3": "large-v3",
        "whisper-large-v3": "large-v3",
        "large-v3": "large-v3",
    }
    return aliases.get(str(raw), str(raw))


def get_whisper_model(
    model_name: Optional[str] = None,
    device: Optional[str] = None,
):
    """Load (and cache) openai-whisper model. Default: large-v3 on CUDA if available."""
    global _whisper_model, _whisper_model_name, _whisper_device

    import torch

    name = _resolve_model_name(model_name)
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    if (
        _whisper_model is not None
        and _whisper_model_name == name
        and _whisper_device == device
    ):
        return _whisper_model

    try:
        import whisper
    except ImportError as e:
        raise ImportError(
            "Install openai-whisper: pip install -r requirements/eval.txt"
        ) from e

    _whisper_model = whisper.load_model(name, device=device)
    _whisper_model_name = name
    _whisper_device = device
    return _whisper_model


def _load_audio_16k(wav_path: Path):
    """Load mono float32 audio at 16 kHz without requiring system ffmpeg."""
    import numpy as np

    try:
        import librosa

        audio, _ = librosa.load(str(wav_path), sr=16000, mono=True)
        return np.asarray(audio, dtype=np.float32)
    except Exception:
        import soundfile as sf

        audio, sr = sf.read(str(wav_path), always_2d=False)
        audio = np.asarray(audio, dtype=np.float32)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        if sr != 16000:
            # linear resample fallback if librosa unavailable
            duration = len(audio) / float(sr)
            n = int(duration * 16000)
            x_old = np.linspace(0.0, 1.0, num=len(audio), endpoint=False)
            x_new = np.linspace(0.0, 1.0, num=n, endpoint=False)
            audio = np.interp(x_new, x_old, audio).astype(np.float32)
        return audio


def transcribe(
    wav_path: str | Path,
    language: Optional[str] = None,
    *,
    model_name: Optional[str] = None,
    device: Optional[str] = None,
) -> str:
    """
    ASR transcription with openai-whisper (default large-v3).

    language: pipeline label or ISO code — en, ar, hi, te (optional hint).
    Loads audio via librosa/soundfile (no system ffmpeg required).
    """
    path = Path(wav_path)
    if not path.is_file():
        raise FileNotFoundError(f"Audio not found: {path}")

    model = get_whisper_model(model_name=model_name, device=device)
    whisper_lang = None
    if language:
        whisper_lang = _LANG_TO_WHISPER.get(language.lower(), language.lower())

    audio = _load_audio_16k(path)
    use_fp16 = (device or _whisper_device or "cuda").startswith("cuda")
    result = model.transcribe(
        audio,
        language=whisper_lang,
        task="transcribe",
        fp16=use_fp16,
    )
    return str(result.get("text", "")).strip()


def round_trip_wer(
    wav_path: str | Path,
    reference_text: str,
    language: Optional[str] = None,
    *,
    model_name: Optional[str] = None,
    device: Optional[str] = None,
) -> dict:
    """Return WER% plus hypothesis/reference for one generated clip."""
    hyp = transcribe(
        wav_path,
        language=language,
        model_name=model_name,
        device=device,
    )
    return {
        "wer_pct": compute_wer(reference_text, hyp),
        "hypothesis": hyp,
        "reference": reference_text,
        "wav_path": str(wav_path),
        "language": language,
        "asr_model": _resolve_model_name(model_name),
    }
