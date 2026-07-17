"""English TTS via Resemble AI Chatterbox — zero-shot clone from reference WAV."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pipelines.base import BaseTTSPipeline
from pipelines.config import load_config, project_root


class EnglishChatterboxPipeline(BaseTTSPipeline):
    """ChatterboxTTS with voice cloning from the assignment reference clip."""

    language = "english"
    model_id = "chatterbox"

    def __init__(
        self,
        reference_wav: str | Path,
        output_dir: str | Path,
        device: str = "cuda",
        exaggeration: float | None = None,
        cfg_weight: float | None = None,
    ) -> None:
        super().__init__(reference_wav, output_dir, device=device)
        cfg = load_config()
        chatter = cfg.get("models", {}).get("chatterbox", {})
        self.exaggeration = (
            exaggeration
            if exaggeration is not None
            else float(chatter.get("exaggeration", 0.5))
        )
        self.cfg_weight = (
            cfg_weight
            if cfg_weight is not None
            else float(chatter.get("cfg_weight", 0.5))
        )
        self._sample_rate: int = 24000

    def load(self) -> None:
        if self._model is not None:
            return

        from chatterbox.tts import ChatterboxTTS

        torch_device = self.device if self.device != "cuda" else "cuda"
        model = ChatterboxTTS.from_pretrained(device=torch_device)
        self._model = model
        self._sample_rate = int(model.sr)
        # Warm speaker conditionals once; generate() still accepts the path.
        model.prepare_conditionals(
            str(self.reference_wav), exaggeration=self.exaggeration
        )

    def _synthesize(self, text: str) -> tuple[np.ndarray, int]:
        assert self._model is not None, "Call load() before synthesize"

        wav = self._model.generate(
            text,
            audio_prompt_path=str(self.reference_wav),
            exaggeration=self.exaggeration,
            cfg_weight=self.cfg_weight,
        )
        # Chatterbox returns a torch tensor shaped [1, T] or [T]
        if hasattr(wav, "detach"):
            audio = wav.detach().cpu().numpy()
        else:
            audio = np.asarray(wav)
        audio = np.asarray(audio, dtype=np.float32).reshape(-1)
        peak = float(np.max(np.abs(audio))) if audio.size else 0.0
        if peak > 1.0:
            audio = audio / peak
        return audio, self._sample_rate


def default_english_chatterbox_pipeline(
    project_root_path: str | Path | None = None,
    device: str = "cuda",
) -> EnglishChatterboxPipeline:
    root = Path(project_root_path) if project_root_path else project_root()
    return EnglishChatterboxPipeline(
        reference_wav=root / "data" / "reference" / "speaker_ref.wav",
        output_dir=root / "outputs" / "english" / "chatterbox",
        device=device,
    )
