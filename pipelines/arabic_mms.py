"""Arabic TTS via Meta MMS-TTS (facebook/mms-tts-ara).

Single-speaker VITS — no reference-WAV cloning. The assignment reference is
kept for BaseTTSPipeline / speaker-similarity eval (expect low cosine).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pipelines.base import BaseTTSPipeline
from pipelines.config import load_config, project_root


class ArabicMmsPipeline(BaseTTSPipeline):
    """Meta MMS-TTS Arabic — fixed speaker, no cloning."""

    language = "arabic"
    model_id = "mms_tts"

    def __init__(
        self,
        reference_wav: str | Path,
        output_dir: str | Path,
        device: str = "cuda",
        model_name: str | None = None,
    ) -> None:
        super().__init__(reference_wav, output_dir, device=device)
        cfg = load_config()
        mms = cfg.get("models", {}).get("mms_tts", {})
        self.model_name = model_name or mms.get(
            "model_name", "facebook/mms-tts-ara"
        )
        self._tokenizer = None
        self._sample_rate: int = 16000

    def load(self) -> None:
        if self._model is not None:
            return

        import torch
        from transformers import AutoTokenizer, VitsModel

        torch_device = self.device if self.device != "cuda" else "cuda"
        model = VitsModel.from_pretrained(self.model_name)
        model = model.to(torch_device)
        model.eval()

        self._model = model
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._sample_rate = int(model.config.sampling_rate)
        self._torch_device = torch_device

    def _synthesize(self, text: str) -> tuple[np.ndarray, int]:
        assert self._model is not None, "Call load() before synthesize"
        assert self._tokenizer is not None

        import torch

        inputs = self._tokenizer(text, return_tensors="pt")
        inputs = {k: v.to(self._torch_device) for k, v in inputs.items()}

        with torch.inference_mode():
            out = self._model(**inputs).waveform

        audio = out.detach().cpu().numpy().squeeze().astype(np.float32)
        peak = float(np.max(np.abs(audio))) if audio.size else 0.0
        if peak > 1.0:
            audio = audio / peak
        return audio, self._sample_rate


def default_arabic_mms_pipeline(
    project_root_path: str | Path | None = None,
    device: str = "cuda",
) -> ArabicMmsPipeline:
    root = Path(project_root_path) if project_root_path else project_root()
    return ArabicMmsPipeline(
        reference_wav=root / "data" / "reference" / "speaker_ref.wav",
        output_dir=root / "outputs" / "arabic" / "mms",
        device=device,
    )
