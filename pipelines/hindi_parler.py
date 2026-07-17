"""Hindi TTS via AI4Bharat Indic Parler-TTS (description / named-speaker style).

Unlike XTTS, this model does not clone from a reference WAV. Speaker identity is
controlled by a text description (e.g. recommended Hindi speakers Rohit / Divya).
The reference WAV is still required by BaseTTSPipeline so eval can score
speaker similarity against the assignment clone target (expect lower cosine).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pipelines.base import BaseTTSPipeline
from pipelines.config import load_config, project_root

# Official Hindi recommended voice from the Indic Parler-TTS model card.
DEFAULT_DESCRIPTION = (
    "Divya's voice is monotone yet slightly fast in delivery, with a very "
    "close recording that almost has no background noise."
)


class HindiParlerPipeline(BaseTTSPipeline):
    """Indic Parler-TTS for Hindi — style/description based, not WAV cloning."""

    language = "hindi"
    model_id = "indic_parler_tts"

    def __init__(
        self,
        reference_wav: str | Path,
        output_dir: str | Path,
        device: str = "cuda",
        model_name: str | None = None,
        description: str | None = None,
    ) -> None:
        super().__init__(reference_wav, output_dir, device=device)
        cfg = load_config()
        parler = cfg.get("models", {}).get("indic_parler_tts", {})
        self.model_name = model_name or parler.get(
            "model_name", "ai4bharat/indic-parler-tts"
        )
        self.description = description or parler.get(
            "default_description", DEFAULT_DESCRIPTION
        )
        self._tokenizer = None
        self._description_tokenizer = None
        self._sample_rate: int = 44100

    def load(self) -> None:
        if self._model is not None:
            return

        import torch
        from parler_tts import ParlerTTSForConditionalGeneration
        from transformers import AutoTokenizer

        torch_device = self.device if self.device != "cuda" else "cuda:0"
        model = ParlerTTSForConditionalGeneration.from_pretrained(self.model_name)
        model = model.to(torch_device)
        model.eval()

        self._model = model
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._description_tokenizer = AutoTokenizer.from_pretrained(
            model.config.text_encoder._name_or_path
        )
        self._sample_rate = int(model.config.sampling_rate)
        self._torch_device = torch_device

    def _synthesize(self, text: str) -> tuple[np.ndarray, int]:
        assert self._model is not None, "Call load() before synthesize"
        assert self._tokenizer is not None
        assert self._description_tokenizer is not None

        import torch

        desc = self._description_tokenizer(
            self.description, return_tensors="pt"
        ).to(self._torch_device)
        prompt = self._tokenizer(text, return_tensors="pt").to(self._torch_device)

        with torch.inference_mode():
            generation = self._model.generate(
                input_ids=desc.input_ids,
                attention_mask=desc.attention_mask,
                prompt_input_ids=prompt.input_ids,
                prompt_attention_mask=prompt.attention_mask,
            )

        audio = generation.detach().cpu().numpy().squeeze().astype(np.float32)
        peak = float(np.max(np.abs(audio))) if audio.size else 0.0
        if peak > 1.0:
            audio = audio / peak
        return audio, self._sample_rate


def default_hindi_parler_pipeline(
    project_root_path: str | Path | None = None,
    device: str = "cuda",
    description: str | None = None,
) -> HindiParlerPipeline:
    root = Path(project_root_path) if project_root_path else project_root()
    return HindiParlerPipeline(
        reference_wav=root / "data" / "reference" / "speaker_ref.wav",
        output_dir=root / "outputs" / "hindi" / "parler",
        device=device,
        description=description,
    )
