# Infinia Voice Pipeline (Track A)

Open-source multilingual TTS with voice cloning for **English, Arabic, Hindi, and Telugu**, benchmarked against the assignment Section 3 metrics.

## Recommended setup (summary)

_TBD after Phase 5 benchmarks. Working assumption: per-language router (XTTS / Indic Parler / etc.), not one model for all languages._

## Hardware

- **GPU (locked):** NVIDIA **RTX PRO 6000 Blackwell Server Edition** (96 GB) on Lightning AI  
- All latency / RTF numbers must be measured on this GPU.

## Environment (Lightning constraint)

Lightning Studios allow **only one** conda/venv (`cloudspace`). Separate per-model envs from the original plan are **not** creatable in this Studio.

```bash
# Already on cloudspace — install shared scaffold deps:
pip install -r requirements/base.txt

# When wiring a model family (Phase 2+), install that family's file:
pip install -r requirements/xtts.txt
# later: parler.txt / eval.txt — watch for dependency conflicts
```

If XTTS and Parler cannot coexist, use a **second Studio** for the conflicting family and keep results comparable by always naming RTX PRO 6000 in the table.

## Layout

```
infinia-voice-pipeline/
├── configs/models.yaml
├── data/reference/speaker_ref.wav
├── data/test_sentences.json
├── pipelines/          # BaseTTSPipeline + language stubs
├── eval/               # WER, similarity, latency/RTF, MOS sheet
├── outputs/{english,arabic,hindi,telugu}/
├── requirements/
└── results/results_table.md
```

## Quick check (Phase 1)

```bash
cd infinia-voice-pipeline
python -c "
from pathlib import Path
from pipelines.base import BaseTTSPipeline, SynthResult
from pipelines.english import default_english_pipeline
p = default_english_pipeline(Path('.'))
print(p.language, p.reference_wav.exists(), p.output_dir)
audio, sr = p.load_reference()
print(f'ref: {len(audio)/sr:.2f}s @ {sr}Hz')
"
```

Language pipelines raise `NotImplementedError` on `load()` / `synth()` until Phase 2+ wires the models.

## Phases

| Phase | Status |
|-------|--------|
| 0 Environment & data | Done (ref wav + test sentences + RTX PRO 6000 decision) |
| 1 Repo scaffold | Done (this tree) |
| 2 English XTTS-v2 | Done through step 4 — WAVs in `outputs/english/xtts/` (`python scripts/run_english.py`) |
| 3 Eval harness | In progress — `python scripts/eval_english.py` (WER + Resemblyzer cosine + latency/RTF) |
| 4 Hindi / Telugu / Arabic | After eval works |
| 5 Compare + winners | |
| 6 Package + write-up | |

## License / cloning note

Reference voice is the author's own recording. Do not use third-party voices without consent.
