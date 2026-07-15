"""Telugu TTS pipeline — Phase 4: Indic Parler-TTS vs MMS-TTS / Indic-TTS.

Note: XTTS-v2 does not support Telugu.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pipelines.base import BaseTTSPipeline


class TeluguPipeline(BaseTTSPipeline):
    language = "telugu"
    model_id = "indic_parler_tts"

    def load(self) -> None:
        raise NotImplementedError(
            "TeluguPipeline.load: wire Indic Parler-TTS (compare MMS) in Phase 4"
        )

    def _synthesize(self, text: str) -> tuple[np.ndarray, int]:
        raise NotImplementedError("TeluguPipeline._synthesize: not implemented yet")


def default_telugu_pipeline(
    project_root: str | Path,
    device: str = "cuda",
) -> TeluguPipeline:
    root = Path(project_root)
    return TeluguPipeline(
        reference_wav=root / "data" / "reference" / "speaker_ref.wav",
        output_dir=root / "outputs" / "telugu" / "parler",
        device=device,
    )
