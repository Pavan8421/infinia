"""Arabic TTS pipeline — Phase 4: XTTS-v2 first, then Fish-Speech / MMS-TTS."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pipelines.base import BaseTTSPipeline


class ArabicPipeline(BaseTTSPipeline):
    language = "arabic"
    model_id = "xtts_v2"

    def load(self) -> None:
        raise NotImplementedError(
            "ArabicPipeline.load: wire XTTS-v2 (then Fish-Speech/MMS) in Phase 4"
        )

    def _synthesize(self, text: str) -> tuple[np.ndarray, int]:
        raise NotImplementedError("ArabicPipeline._synthesize: not implemented yet")


def default_arabic_pipeline(
    project_root: str | Path,
    device: str = "cuda",
) -> ArabicPipeline:
    root = Path(project_root)
    return ArabicPipeline(
        reference_wav=root / "data" / "reference" / "speaker_ref.wav",
        output_dir=root / "outputs" / "arabic" / "xtts",
        device=device,
    )
