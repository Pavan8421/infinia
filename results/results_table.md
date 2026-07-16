# Results table — Section 3 metrics

Hardware: NVIDIA RTX PRO 6000 Blackwell Server Edition (96 GB) on Lightning AI  
Reference: `data/reference/speaker_ref.wav`  
Source JSON: `results/english_xtts_eval.json` (from `python scripts/eval_english.py`)  
ASR: Whisper large-v3 · Speaker sim: Resemblyzer · Number-word normalization applied for WER

## Summary (averages vs targets)

| Language | Model | MOS (≥4.0) | Speaker sim (≥0.75) | Latency (batch, &lt;2s) | RTF (≤0.5) | WER (≤10%) | Notes |
|----------|-------|------------|---------------------|------------------------|------------|------------|-------|
| English | xtts_v2 | *pending* (Phase 3 step 6) | **0.79** ✓ | **0.70–1.44 s** ✓ | **0.21** ✓ | **0.0%** ✓ | WAVs in `outputs/english/xtts/`. Cosine avg meets target; en_1 alone is 0.75 (borderline). Listener said clone is only moderately similar — report both. |
| Hindi | indic_parler_tts | — | — | — | — | — | Phase 4 |
| Hindi | xtts_v2 | — | — | — | — | — | Phase 4 compare |
| Telugu | indic_parler_tts | — | — | — | — | — | Phase 4 |
| Telugu | mms_tts | — | — | — | — | — | Phase 4 compare |
| Arabic | xtts_v2 | — | — | — | — | — | Phase 4 |
| Arabic | fish_speech / mms | — | — | — | — | — | Phase 4 compare |

## English · xtts_v2 — per clip

| Clip | WER | Cosine | Gen time | Duration | RTF | Cosine ≥0.75 |
|------|-----|--------|----------|----------|-----|--------------|
| en_1 | 0.0% | 0.746 | 1.44 s | 5.29 s | 0.273 | borderline miss |
| en_2 | 0.0% | 0.811 | 0.95 s | 5.15 s | 0.185 | ✓ |
| en_3 | 0.0% | 0.814 | 0.70 s | 3.80 s | 0.185 | ✓ |
| **AVG** | **0.0%** | **0.790** | — | — | **0.214** | ✓ avg |

Targets hit for English (auto metrics): latency, RTF, WER, speaker sim (average). MOS still open.

## Winners (fill in Phase 5)

| Language | Winner | One-line reason |
|----------|--------|-----------------|
| English | TBD | |
| Hindi | TBD | |
| Telugu | TBD | |
| Arabic | TBD | |
