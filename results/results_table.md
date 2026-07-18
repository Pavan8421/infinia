# Results table — Section 3 metrics

Hardware: NVIDIA RTX PRO 6000 Blackwell Server Edition (96 GB) on Lightning AI  
Reference: `data/reference/speaker_ref.wav`  
Source JSONs: `results/english_xtts_eval.json`, `english_chatterbox_eval.json`, `arabic_xtts_eval.json`, `arabic_mms_eval.json`, `hindi_xtts_eval.json`, `hindi_parler_eval.json`  
ASR: Whisper large-v3 · Speaker sim: Resemblyzer · EN number-word normalization for WER  

**XTTS rows refreshed** after re-synth + `eval_{english,arabic,hindi}.py` (Chatterbox / Parler / MMS rows unchanged from prior evals).

## Summary (averages vs targets)

| Language | Model | MOS (≥4.0) | Speaker sim (≥0.75) | Latency (batch, &lt;2s) | RTF (≤0.5) | WER (≤10%) | Notes |
|----------|-------|------------|---------------------|------------------------|------------|------------|-------|
| English | xtts_v2 | **3.0** ✗ | **0.80** ✓ | **0.70–1.44 s** ✓ | **0.21** ✓ | **0.0%** ✓ | Re-eval auto metrics OK. MOS: clone weak — sounds like a different speaker (avg 3.0/5). |
| English | chatterbox | **4.3** ✓ | **0.88** ✓ | **1.09–1.55 s** ✓ | **0.48** ✓ | **4.8%** ✓ | MOS: clone matches ref; en_2/en_3 somewhat fast (scores 5/4/4). Stronger speaker sim + human clone judgment than XTTS. |
| Hindi | indic_parler_tts | **3.0** ✗ | **0.51** ✗ | **2.75–3.99 s** ✗ | **0.75** ✗ | **36.7%** ✗ | No clone (Divya). MOS: robotic + very low volume (3/3/3). Cosine informational. |
| Hindi | xtts_v2 | **4.0** ✓ | **0.86** ✓ | **1.05–1.59 s** ✓ | **0.19** ✓ | **40.0%** ✗ | MOS 5/4/3: good clone+speed; hi_2 Rahul unclear; hi_3 voice breaks. WER still high (ASR). |
| Arabic | xtts_v2 | **4.0** ✓ | **0.79** ✓ | **0.58–1.26 s** ✓ | **0.20** ✓ | **0.0%** ✓ | MOS: natural + clone OK. Listener does not know Arabic (naturalness/clone only; intelligibility via WER). |
| Arabic | mms_tts | **4.0** ✓ | **0.54** ✗ | **0.08–0.66 s** ✓ | **0.06** ✓ | **38.1%** ✗ | MOS: smooth/natural; no clone. Listener does not know Arabic. Cosine informational. Fastest RTF. |

**English compare note:** Chatterbox wins human clone + MOS (4.3 vs XTTS 3.0); XTTS still better WER/RTF. Listener: XTTS clone fails A/B (“different voice”); Chatterbox clone good but can sound fast.  
**Hindi compare note:** XTTS = clone; Parler = fixed Divya. Speaker-sim applies to XTTS only.  
**Arabic compare note:** Listener does not know Arabic — MOS is naturalness/clone only; intelligibility from Whisper WER. XTTS wins on WER (0% vs 38%) + cloning; MMS ties MOS (4.0) and wins raw speed.  

## English · xtts_v2 — per clip

Source: `results/english_xtts_eval.json` (re-eval).

| Clip | WER | Cosine | Gen time | Duration | RTF | Cosine ≥0.75 |
|------|-----|--------|----------|----------|-----|--------------|
| en_1 | 0.0% | 0.761 | 1.44 s | 5.29 s | 0.273 | ✓ |
| en_2 | 0.0% | 0.823 | 0.95 s | 5.15 s | 0.185 | ✓ |
| en_3 | 0.0% | 0.806 | 0.70 s | 3.80 s | 0.185 | ✓ |
| **AVG** | **0.0%** | **0.797** | — | — | **0.214** | ✓ |

## English · chatterbox — per clip

Zero-shot clone from reference. Source: `results/english_chatterbox_eval.json` (unchanged).

| Clip | WER | Cosine | Gen time | Duration | RTF | Notes |
|------|-----|--------|----------|----------|-----|-------|
| en_1 | 0.0% | 0.892 | 1.55 s | 2.68 s | 0.578 | RTF alone above 0.5 |
| en_2 | 14.3% | 0.875 | 1.32 s | 3.20 s | 0.412 | Whisper: `Rahul`→`Vlahool` |
| en_3 | 0.0% | 0.862 | 1.09 s | 2.44 s | 0.448 | clean |
| **AVG** | **4.8%** | **0.876** | — | — | **0.479** | sim/latency/WER/RTF (avg) ✓ |

## Arabic · xtts_v2 — per clip

Cross-lingual cloning from English reference → MSA. Source: `results/arabic_xtts_eval.json` (re-eval).

| Clip | WER | Cosine | Gen time | Duration | RTF | Notes |
|------|-----|--------|----------|----------|-----|-------|
| ar_1 | 0.0% | 0.827 | 1.26 s | 4.86 s | 0.259 | exact ASR match |
| ar_2 | 0.0% | 0.757 | 0.78 s | 4.64 s | 0.169 | exact ASR match |
| ar_3 | 0.0% | 0.786 | 0.58 s | 3.38 s | 0.173 | exact ASR match |
| **AVG** | **0.0%** | **0.790** | — | — | **0.200** | all Section 3 auto targets ✓ |

## Arabic · mms_tts — per clip

Fixed MMS Arabic speaker; not WAV cloning. Source: `results/arabic_mms_eval.json` (unchanged).

| Clip | WER | Cosine (vs ref) | Gen time | Duration | RTF | Notes |
|------|-----|-----------------|----------|----------|-----|-------|
| ar_1 | 42.9% | 0.558 | 0.66 s | 5.02 s | 0.131 | ASR garbled start |
| ar_2 | 28.6% | 0.521 | 0.08 s | 5.15 s | 0.016 | ASR: `اتصل`→`الصل` |
| ar_3 | 42.9% | 0.556 | 0.21 s | 4.86 s | 0.043 | ASR mangled opening |
| **AVG** | **38.1%** | **0.545** | — | — | **0.063** | latency/RTF ✓; WER + sim miss |

## Hindi · xtts_v2 — per clip

Cross-lingual cloning from reference → Hindi. Source: `results/hindi_xtts_eval.json` (re-eval).

| Clip | WER | Cosine | Gen time | Duration | RTF | Notes |
|------|-----|--------|----------|----------|-----|-------|
| hi_1 | 30.0% | 0.865 | 1.59 s | 6.77 s | 0.235 | Whisper: `मौसम`→`मोसम`, `सैर`→`सेर` |
| hi_2 | 60.0% | 0.859 | 1.05 s | 6.22 s | 0.169 | Whisper: numbers→`247`, `कृपया` mangled |
| hi_3 | 30.0% | 0.844 | 1.09 s | 6.44 s | 0.170 | Whisper: `खिड़की`→`खिरकी` |
| **AVG** | **40.0%** | **0.856** | — | — | **0.191** | latency/RTF/sim ✓; WER still above 10% |

## Hindi · indic_parler_tts — per clip

Named-speaker Divya; not WAV cloning. Source: `results/hindi_parler_eval.json` (unchanged).

| Clip | WER | Cosine (vs ref) | Gen time | Duration | RTF | Notes |
|------|-----|-----------------|----------|----------|-----|-------|
| hi_1 | 30.0% | 0.495 | 3.04 s | 3.60 s | 0.843 | ASR near-misses |
| hi_2 | 60.0% | 0.541 | 3.99 s | 5.46 s | 0.732 | ASR: numbers→`247` |
| hi_3 | 20.0% | 0.494 | 2.75 s | 4.12 s | 0.667 | ASR: `खिड़की`→`खिरकी` |
| **AVG** | **36.7%** | **0.510** | — | — | **0.747** | WER slightly better than XTTS; latency/RTF/sim miss |

## Winners (fill in Phase 5)

| Language | Winner | One-line reason |
|----------|--------|-----------------|
| English | **chatterbox** | Best human clone + MOS (4.3); cosine 0.88. XTTS wins WER/RTF but clone fails listening test. |
| Hindi | **xtts_v2** | MOS 4.0 + real clone vs Parler 3.0 (robotic/quiet, no clone). WER still weak on both. |
| Arabic | **xtts_v2** | MOS tied (4.0); XTTS wins clone + WER 0%. Listener non-Arabic; MOS = naturalness/clone only. |
