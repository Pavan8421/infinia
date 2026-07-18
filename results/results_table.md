# Results table — Section 3 metrics

Hardware: NVIDIA RTX PRO 6000 Blackwell Server Edition (96 GB) on Lightning AI  
Reference: `data/reference/speaker_ref.wav`  
Source JSONs: `results/english_xtts_eval.json`, `english_chatterbox_eval.json`, `arabic_xtts_eval.json`, `arabic_mms_eval.json`, `hindi_xtts_eval.json`, `hindi_parler_eval.json`  
ASR: Whisper large-v3 · Speaker sim: Resemblyzer · EN number-word normalization for WER

## Summary (averages vs targets)

| Language | Model | MOS (≥4.0) | Speaker sim (≥0.75) | Latency (batch, &lt;2s) | RTF (≤0.5) | WER (≤10%) | Notes |
|----------|-------|------------|---------------------|------------------------|------------|------------|-------|
| English | xtts_v2 | *pending* | **0.79** ✓ | **0.70–1.44 s** ✓ | **0.21** ✓ | **0.0%** ✓ | Same ref clone. Best WER + RTF. Cosine avg OK; en_1 borderline 0.75. |
| English | chatterbox | *pending* | **0.88** ✓ | **1.09–1.55 s** ✓ | **0.48** ✓ | **4.8%** ✓ | Zero-shot clone from same ref. Stronger speaker sim than XTTS; WER hit on `Rahul`→`Vlahool` (en_2). en_1 RTF 0.58 alone misses; avg OK. WAVs in `outputs/english/chatterbox/`. |
| Hindi | indic_parler_tts | *pending* | **0.51** ✗ | **2.75–3.99 s** ✗ | **0.75** ✗ | **36.7%** ✗ | Named-speaker **Divya** (description), **not** WAV clone. Cosine vs ref informational. WER better than Hindi XTTS (50%); latency/RTF worse. |
| Hindi | xtts_v2 | *pending* | **0.86** ✓ | **1.01–1.59 s** ✓ | **0.21** ✓ | **50.0%** ✗ | Cross-lingual clone. Wins clone + speed vs Parler; loses on raw WER. |
| Arabic | xtts_v2 | *pending* | **0.81** ✓ | **0.69–1.65 s** ✓ | **0.22** ✓ | **23.8%** ✗ | Cross-lingual clone. Better WER than MMS; wins clone. |
| Arabic | mms_tts | *pending* | **0.54** ✗ | **0.08–0.66 s** ✓ | **0.06** ✓ | **38.1%** ✗ | Fixed MMS speaker (`facebook/mms-tts-ara`), **not** clone. Fastest RTF/latency of AR pair; worse WER + no clone. WAVs in `outputs/arabic/mms/`. |

**English compare note:** Both clone the same reference. Chatterbox wins speaker similarity; XTTS wins WER and RTF. Pick after MOS listen.  
**Hindi compare note:** XTTS = clone; Parler = fixed Divya. Speaker-sim target applies to XTTS only.  
**Arabic compare note:** XTTS = clone of ref; MMS = fixed speaker. Speaker-sim applies to XTTS only. MMS wins speed; XTTS wins WER + clone.

## English · xtts_v2 — per clip

| Clip | WER | Cosine | Gen time | Duration | RTF | Cosine ≥0.75 |
|------|-----|--------|----------|----------|-----|--------------|
| en_1 | 0.0% | 0.746 | 1.44 s | 5.29 s | 0.273 | borderline miss |
| en_2 | 0.0% | 0.811 | 0.95 s | 5.15 s | 0.185 | ✓ |
| en_3 | 0.0% | 0.814 | 0.70 s | 3.80 s | 0.185 | ✓ |
| **AVG** | **0.0%** | **0.790** | — | — | **0.214** | ✓ avg |

## English · chatterbox — per clip

Zero-shot clone from reference. Source: `results/english_chatterbox_eval.json`.

| Clip | WER | Cosine | Gen time | Duration | RTF | Notes |
|------|-----|--------|----------|----------|-----|-------|
| en_1 | 0.0% | 0.892 | 1.55 s | 2.68 s | 0.578 | RTF alone above 0.5 |
| en_2 | 14.3% | 0.875 | 1.32 s | 3.20 s | 0.412 | Whisper: `Rahul`→`Vlahool`; `247` OK |
| en_3 | 0.0% | 0.862 | 1.09 s | 2.44 s | 0.448 | clean |
| **AVG** | **4.8%** | **0.876** | — | — | **0.479** | sim/latency/WER/RTF (avg) ✓ |

## Arabic · xtts_v2 — per clip

Cross-lingual cloning from English reference → MSA. Source: `results/arabic_xtts_eval.json`.

| Clip | WER | Cosine | Gen time | Duration | RTF | Notes |
|------|-----|--------|----------|----------|-----|-------|
| ar_1 | 42.9% | 0.846 | 1.65 s | 5.24 s | 0.316 | Whisper typo `التقس` / split `مناسب` |
| ar_2 | 28.6% | 0.767 | 0.77 s | 4.45 s | 0.173 | Whisper wrote `25` vs `خمسة وعشرين` |
| ar_3 | 0.0% | 0.803 | 0.69 s | 3.99 s | 0.173 | clean |
| **AVG** | **23.8%** | **0.805** | — | — | **0.220** | latency/RTF/sim ✓; WER above 10% target |

## Arabic · mms_tts — per clip

Fixed MMS Arabic speaker (`facebook/mms-tts-ara`); not WAV cloning. Source: `results/arabic_mms_eval.json`. Cosine vs assignment reference is informational.

| Clip | WER | Cosine (vs ref) | Gen time | Duration | RTF | Notes |
|------|-----|-----------------|----------|----------|-----|-------|
| ar_1 | 42.9% | 0.558 | 0.66 s | 5.02 s | 0.131 | ASR garbled start (`ويأتي التقص` / `جميلي`) |
| ar_2 | 28.6% | 0.521 | 0.08 s | 5.15 s | 0.016 | ASR: `اتصل`→`الصل`; numbers spoken OK |
| ar_3 | 42.9% | 0.556 | 0.21 s | 4.86 s | 0.043 | ASR mangled opening (`تحنى في ذتي`) |
| **AVG** | **38.1%** | **0.545** | — | — | **0.063** | latency/RTF ✓; WER + sim miss (sim expected) |

## Hindi · xtts_v2 — per clip

Cross-lingual cloning from reference → Hindi. Source: `results/hindi_xtts_eval.json`.

| Clip | WER | Cosine | Gen time | Duration | RTF | Notes |
|------|-----|--------|----------|----------|-----|-------|
| hi_1 | 40.0% | 0.855 | 1.59 s | 5.98 s | 0.265 | Whisper: `मौसम`→`मोसम`, `सैर`→`सेल` |
| hi_2 | 60.0% | 0.855 | 1.04 s | 5.52 s | 0.188 | Whisper: `चौबीस सात`→`24`, `कृपया`→`प्रिप्या` |
| hi_3 | 50.0% | 0.861 | 1.01 s | 5.47 s | 0.185 | Whisper: `खिड़की`→`किरकी` |
| **AVG** | **50.0%** | **0.857** | — | — | **0.213** | latency/RTF/sim ✓; WER above 10% |

## Hindi · indic_parler_tts — per clip

Named-speaker **Divya** (description); not WAV cloning. Source: `results/hindi_parler_eval.json`. Speaker cosine vs assignment reference is informational.

| Clip | WER | Cosine (vs ref) | Gen time | Duration | RTF | Notes |
|------|-----|-----------------|----------|----------|-----|-------|
| hi_1 | 30.0% | 0.495 | 3.04 s | 3.60 s | 0.843 | ASR: `बाहर`→`बहार`, `सैर`→`सेर` |
| hi_2 | 60.0% | 0.541 | 3.99 s | 5.46 s | 0.732 | ASR: `चौबीस सात`→`247`, name near-miss |
| hi_3 | 20.0% | 0.494 | 2.75 s | 4.12 s | 0.667 | ASR: `खिड़की`→`खिरकी` |
| **AVG** | **36.7%** | **0.510** | — | — | **0.747** | WER better than XTTS; latency/RTF/sim miss (sim expected) |

## Winners (fill in Phase 5)

| Language | Winner | One-line reason |
|----------|--------|-----------------|
| English | TBD | Auto metrics: Chatterbox better clone (0.88 vs 0.79); XTTS better WER/RTF — decide after MOS |
| Hindi | TBD | Tentative: **XTTS if cloning required**; Parler if native Hindi naturalness/WER after MOS |
| Arabic | TBD | Tentative: **XTTS if cloning / better WER**; MMS if raw speed (RTF 0.06) — decide after MOS |
