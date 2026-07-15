"""English TTS pipeline — XTTS-v2 (coqui-tts) with voice cloning."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pipelines.base import BaseTTSPipeline
from pipelines.config import load_config, project_root


class EnglishPipeline(BaseTTSPipeline):
    language = "english"
    model_id = "xtts_v2"
    xtts_language = "en"

    def __init__(
        self,
        reference_wav: str | Path,
        output_dir: str | Path,
        device: str = "cuda",
        model_name: str | None = None,
    ) -> None:
        super().__init__(reference_wav, output_dir, device=device)
        cfg = load_config()
        xtts = cfg.get("models", {}).get("xtts_v2", {})
        self.model_name = model_name or xtts.get(
            "model_name", "tts_models/multilingual/multi-dataset/xtts_v2"
        )
        self._sample_rate: int = 24000

    def load(self) -> None:
        if self._model is not None:
            return
        import os

        from TTS.api import TTS

        # Non-interactive CPML acceptance (https://coqui.ai/cpml). Required for XTTS download.
        os.environ.setdefault("COQUI_TOS_AGREED", "1")

        use_gpu = self.device.startswith("cuda")
        # Prefer .to(device); gpu= kwarg is deprecated in coqui-tts 0.27
        tts = TTS(model_name=self.model_name, progress_bar=True, gpu=False)
        if use_gpu:
            tts.to(self.device)
        self._model = tts
        # XTTS-v2 synthesizes at 24 kHz
        self._sample_rate = 24000

    def _synthesize(self, text: str) -> tuple[np.ndarray, int]:
        assert self._model is not None, "Call load() before synthesize"
        wav = self._model.tts(
            text=text,
            speaker_wav=str(self.reference_wav),
            language=self.xtts_language,
        )
        audio = np.asarray(wav, dtype=np.float32).reshape(-1)
        peak = float(np.max(np.abs(audio))) if audio.size else 0.0
        if peak > 1.0:
            audio = audio / peak
        return audio, self._sample_rate


def default_english_pipeline(
    project_root_path: str | Path | None = None,
    device: str = "cuda",
) -> EnglishPipeline:
    root = Path(project_root_path) if project_root_path else project_root()
    return EnglishPipeline(
        reference_wav=root / "data" / "reference" / "speaker_ref.wav",
        output_dir=root / "outputs" / "english" / "xtts",
        device=device,
    )
