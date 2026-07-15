"""Shared TTS pipeline interface: load reference, synthesize, time latency/RTF."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import numpy as np
import soundfile as sf


@dataclass
class SynthResult:
    """Output of a single synthesis call plus timing for Section 3 metrics."""

    wav_path: Path
    sample_rate: int
    gen_time_sec: float
    audio_duration_sec: float
    latency_to_first_chunk_sec: Optional[float] = None  # streaming only
    mode: str = "batch"  # "batch" | "streaming"
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def rtf(self) -> float:
        """Real-time factor: generation_time / audio_length. Target ≤ 0.5."""
        if self.audio_duration_sec <= 0:
            return float("inf")
        return self.gen_time_sec / self.audio_duration_sec


class BaseTTSPipeline(ABC):
    """Common interface every language pipeline implements."""

    language: str = "unknown"
    model_id: str = "unknown"

    def __init__(
        self,
        reference_wav: str | Path,
        output_dir: str | Path,
        device: str = "cuda",
    ) -> None:
        self.reference_wav = Path(reference_wav)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.device = device
        self._model: Any = None

        if not self.reference_wav.is_file():
            raise FileNotFoundError(f"Reference wav not found: {self.reference_wav}")

    @abstractmethod
    def load(self) -> None:
        """Load model weights onto `self.device`. Idempotent preferred."""

    @abstractmethod
    def _synthesize(self, text: str) -> tuple[np.ndarray, int]:
        """
        Run the underlying model.

        Returns:
            audio: float32 mono waveform in [-1, 1]
            sample_rate: int
        """

    def synth(
        self,
        text: str,
        *,
        utterance_id: Optional[str] = None,
        out_name: Optional[str] = None,
    ) -> SynthResult:
        """
        Synthesize `text` cloned toward the reference voice.

        Writes a WAV under `output_dir` and returns paths + timing hooks
        used by eval/latency_rtf.py.
        """
        if self._model is None:
            self.load()

        t0 = time.perf_counter()
        audio, sr = self._synthesize(text)
        gen_time = time.perf_counter() - t0

        audio = np.asarray(audio, dtype=np.float32).reshape(-1)
        duration = float(len(audio) / sr) if sr else 0.0

        stem = out_name or utterance_id or f"{self.language}_{int(time.time())}"
        wav_path = self.output_dir / f"{stem}.wav"
        sf.write(str(wav_path), audio, sr)

        return SynthResult(
            wav_path=wav_path,
            sample_rate=sr,
            gen_time_sec=gen_time,
            audio_duration_sec=duration,
            latency_to_first_chunk_sec=None,
            mode="batch",
            meta={"language": self.language, "model_id": self.model_id, "text": text},
        )

    def load_reference(self) -> tuple[np.ndarray, int]:
        """Load the reference clip as mono float32."""
        audio, sr = sf.read(str(self.reference_wav), always_2d=False)
        audio = np.asarray(audio, dtype=np.float32)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        return audio, int(sr)
