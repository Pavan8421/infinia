# Results table — Section 3 metrics

Hardware: NVIDIA RTX PRO 6000 Blackwell Server Edition (96 GB) on Lightning AI  
Reference: `data/reference/speaker_ref.wav`  
Source JSONs: `results/english_xtts_eval.json`, `arabic_xtts_eval.json`, `hindi_xtts_eval.json`  
ASR: Whisper large-v3 · Speaker sim: Resemblyzer · EN number-word normalization for WER

## Summary (averages vs targets)

| Language | Model | MOS (≥4.0) | Speaker sim (≥0.75) | Latency (batch, &lt;2s) | RTF (≤0.5) | WER (≤10%) | Notes |
|----------|-------|------------|---------------------|------------------------|------------|------------|-------|
| English | xtts_v2 | *pending* (Phase 3 step 6) | **0.79** ✓ | **0.70–1.44 s** ✓ | **0.21** ✓ | **0.0%** ✓ | WAVs in `outputs/english/xtts/`. Cosine avg meets target; en_1 alone is 0.75 (borderline). Listener said clone is only moderately similar — report both. |
| Hindi | indic_parler_tts | — | — | — | — | — | Phase 4 |
| Hindi | xtts_v2 | *pending* | **0.86** ✓ | **1.01–1.59 s** ✓ | **0.21** ✓ | **50.0%** ✗ | Hindi steps 1–4. Cross-lingual clone. High WER largely ASR near-misses (`मौसम`→`मोसम`, `चौबीस सात`→`24`). Listen before blaming TTS. Parler compare still open. |
| Telugu | — | — | — | — | — | — | **Out of scope** (bonus skipped; EN/AR/HI only) |
| Telugu | — | — | — | — | — | — | — |
| Arabic | xtts_v2 | *pending* | **0.81** ✓ | **0.69–1.65 s** ✓ | **0.22** ✓ | **23.8%** ✗ | Phase 4 step 1. Cross-lingual clone. WER miss: ASR typos + `خمسة وعشرين`→`25`; listen before blaming TTS. See per-clip below. |
| Arabic | fish_speech / mms | — | — | — | — | — | Phase 4 compare |

## English · xtts_v2 — per clip

| Clip | WER | Cosine | Gen time | Duration | RTF | Cosine ≥0.75 |
|------|-----|--------|----------|----------|-----|--------------|
| en_1 | 0.0% | 0.746 | 1.44 s | 5.29 s | 0.273 | borderline miss |
| en_2 | 0.0% | 0.811 | 0.95 s | 5.15 s | 0.185 | ✓ |
| en_3 | 0.0% | 0.814 | 0.70 s | 3.80 s | 0.185 | ✓ |
| **AVG** | **0.0%** | **0.790** | — | — | **0.214** | ✓ avg |

Targets hit for English (auto metrics): latency, RTF, WER, speaker sim (average). MOS still open.

## Arabic · xtts_v2 — per clip (Phase 4 step 1)

Cross-lingual cloning from English reference → MSA. Source: `results/arabic_xtts_eval.json`.

| Clip | WER | Cosine | Gen time | Duration | RTF | Notes |
|------|-----|--------|----------|----------|-----|-------|
| ar_1 | 42.9% | 0.846 | 1.65 s | 5.24 s | 0.316 | Whisper typo `التقس` / split `مناسب` |
| ar_2 | 28.6% | 0.767 | 0.77 s | 4.45 s | 0.173 | Whisper wrote `25` vs `خمسة وعشرين` |
| ar_3 | 0.0% | 0.803 | 0.69 s | 3.99 s | 0.173 | clean |
| **AVG** | **23.8%** | **0.805** | — | — | **0.220** | latency/RTF/sim ✓; WER above 10% target |

## Hindi · xtts_v2 — per clip (Phase 4 Hindi step 4)

Cross-lingual cloning from reference → Hindi. Source: `results/hindi_xtts_eval.json`.

| Clip | WER | Cosine | Gen time | Duration | RTF | Notes |
|------|-----|--------|----------|----------|-----|-------|
| hi_1 | 40.0% | 0.855 | 1.59 s | 5.98 s | 0.265 | Whisper: `मौसम`→`मोसम`, `सैर`→`सेल` |
| hi_2 | 60.0% | 0.855 | 1.04 s | 5.52 s | 0.188 | Whisper: `चौबीस सात`→`24`, `कृपया`→`प्रिप्या` |
| hi_3 | 50.0% | 0.861 | 1.01 s | 5.47 s | 0.185 | Whisper: `खिड़की`→`किरकी` |
| **AVG** | **50.0%** | **0.857** | — | — | **0.213** | latency/RTF/sim ✓; WER above 10% |

## Winners (fill in Phase 5)

| Language | Winner | One-line reason |
|----------|--------|-----------------|
| English | TBD | |
| Hindi | TBD | |
| Telugu | — | — |
| Arabic | TBD | |
