"""Hindi TTS pipeline — Phase 4: Indic Parler-TTS vs XTTS-v2."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pipelines.base import BaseTTSPipeline


class HindiPipeline(BaseTTSPipeline):
    language = "hindi"
    model_id = "indic_parler_tts"

    def load(self) -> None:
        raise NotImplementedError(
            "HindiPipeline.load: wire Indic Parler-TTS (compare XTTS) in Phase 4"
        )

    def _synthesize(self, text: str) -> tuple[np.ndarray, int]:
        raise NotImplementedError("HindiPipeline._synthesize: not implemented yet")


def default_hindi_pipeline(
    project_root: str | Path,
    device: str = "cuda",
) -> HindiPipeline:
    root = Path(project_root)
    return HindiPipeline(
        reference_wav=root / "data" / "reference" / "speaker_ref.wav",
        output_dir=root / "outputs" / "hindi" / "parler",
        device=device,
    )
