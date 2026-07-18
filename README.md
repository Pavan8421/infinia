# Infinia Voice Pipeline (Track A)

Open-source multilingual TTS with voice cloning for **English, Arabic, and Hindi**, benchmarked against the assignment Section 3 metrics. Telugu was out of scope.

## Recommended setup (summary)

Use a **per-language router**, not one model for all three languages. On NVIDIA **RTX PRO 6000 Blackwell (96 GB)** with our own reference clip (`data/reference/speaker_ref.wav`): **English → Chatterbox** (best human clone + MOS 4.3; cosine 0.88 — XTTS was faster/cleaner on WER but failed the listening clone test); **Hindi → XTTS-v2** (MOS 4.0 + real zero-shot clone; Indic Parler was robotic/quiet, no clone); **Arabic → XTTS-v2** (MOS 4.0, speaker sim 0.79, **WER 0%**; MMS was smooth and faster but no clone and WER ~38%). Eval tooling: Whisper large-v3 (WER), Resemblyzer (speaker cosine), batch latency/RTF; MOS from one listener (Arabic scored as naturalness/clone only — listener is not an Arabic speaker). Full numbers: [`results/results_table.md`](results/results_table.md).

## Hardware & reproducibility

| Item | Value |
|------|--------|
| GPU | NVIDIA RTX PRO 6000 Blackwell Server Edition (96 GB) · Lightning AI |
| Reference | Own voice · `data/reference/speaker_ref.wav` (~23 s mono) |
| Test set | Locked · `data/test_sentences.json` (3 sentences / language) |
| Config | `configs/models.yaml` (model IDs, pins, params) |

All latency / RTF numbers in the results table were measured on this GPU.

## Models compared

| Language | Models | Winner |
|----------|--------|--------|
| English | XTTS-v2, Chatterbox | **Chatterbox** |
| Hindi | XTTS-v2, Indic Parler-TTS (Divya description) | **XTTS-v2** |
| Arabic | XTTS-v2, Meta MMS-TTS (`facebook/mms-tts-ara`) | **XTTS-v2** |

**Cloning note:** XTTS and Chatterbox clone from the reference WAV. Parler and MMS do **not** — speaker-similarity vs the reference is informational for those two.

## Results

See **[`results/results_table.md`](results/results_table.md)** for Section 3 metrics (MOS, speaker sim, latency, RTF, WER) and per-clip tables.  
Eval JSONs live under `results/*_eval.json`. Sample WAVs under `outputs/{english,arabic,hindi}/…`. MOS sheet: `eval/mos_sheet.csv`.

## Setup

Lightning Studios expose a single `cloudspace` env. Model families **conflict** on `transformers` / torch pins — install one family at a time. Keep **torch 2.8.0+cu128** for Blackwell (`sm_120`); do not let packages downgrade to torch 2.6+cu124.

```bash
cd infinia   # repo root
pip install -r requirements/base.txt
pip install -r requirements/eval.txt
```

Then install **one** generation stack as needed:

```bash
# XTTS (EN / AR / HI) — transformers>=4.57,<5
pip install -r requirements/xtts.txt

# Chatterbox (EN) — after install, restore Blackwell torch if needed:
#   pip install torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 \
#     --index-url https://download.pytorch.org/whl/cu128
pip install -r requirements/chatterbox.txt

# Indic Parler (HI) — transformers==4.46.1 (breaks XTTS until you pin back)
pip install -r requirements/parler.txt
pip install 'transformers==4.46.1'

# MMS Arabic — uses transformers + torch only (see requirements/mms.txt)
```

Gated models: accept access + `huggingface-cli login` for `ai4bharat/indic-parler-tts`.

## Reproduce (generate + eval)

```bash
# --- XTTS ---
python scripts/run_english.py --device cuda
python scripts/run_arabic.py --device cuda
python scripts/run_hindi.py --device cuda
python scripts/eval_english.py --device cuda
python scripts/eval_arabic.py --device cuda
python scripts/eval_hindi.py --device cuda

# --- English Chatterbox ---
python scripts/run_english_chatterbox.py --device cuda
python scripts/eval_english_chatterbox.py --device cuda

# --- Hindi Parler (after transformers==4.46.1) ---
python scripts/run_hindi_parler.py --device cuda
python scripts/eval_hindi_parler.py --device cuda

# --- Arabic MMS ---
python scripts/run_arabic_mms.py --device cuda
python scripts/eval_arabic_mms.py --device cuda
```

Outputs: `outputs/<lang>/<model>/*.wav` + `timings.json`.  
Metrics: `results/<lang>_<model>_eval.json`.

## Layout

```
infinia/
├── README.md
├── configs/models.yaml
├── data/reference/speaker_ref.wav
├── data/test_sentences.json
├── pipelines/          # XTTS, Chatterbox, Parler, MMS
├── eval/               # WER, similarity, latency/RTF, mos_sheet.csv
├── scripts/            # run_* + eval_*
├── outputs/{english,arabic,hindi}/…
├── requirements/
└── results/results_table.md
```

## Failure modes

Honest limits we hit during benchmarking and listening:

| Area | What broke / hurt |
|------|-------------------|
| **English XTTS clone** | Auto cosine looked OK (~0.80), but human A/B said it sounded like a **different speaker** (MOS 3.0). Do not trust cosine alone. |
| **English Chatterbox** | Strong clone (MOS 4.3, cosine 0.88); **en_2 / en_3** felt **too fast**; WER 14% on `Rahul`→`Vlahool`. |
| **Hindi names** | XTTS **hi_2**: “Rahul” unclear to the listener; Whisper often collapses spoken numbers (`चौबीस सात`→`247`). |
| **Hindi prosody** | XTTS **hi_3**: audible **breaks / discontinuities** in the voice (MOS 3 on that clip). |
| **Hindi WER** | Both XTTS (~40%) and Parler (~37%) miss the 10% target; many errors look like **ASR near-misses**, not only TTS. |
| **Parler (Hindi)** | No cloning; MOS 3.0 — **robotic** and **very low volume**. |
| **Arabic MMS** | No cloning; smooth MOS 4.0 but **WER ~38%**; intelligibility judged via ASR (listener is not an Arabic speaker). |
| **Cross-lingual clone** | One English reference → AR/HI XTTS. Works for Arabic in our re-eval (WER 0%); Hindi remains harder. |
| **Dependency hell** | XTTS needs `transformers` 4.57.x; Parler needs **exactly** 4.46.1; Chatterbox may pull torch 2.6 (breaks Blackwell). Sequential installs / pin restores required. |
| **Streaming latency** | We report **batch** full-clip time (&lt;2 s target), not &lt;500 ms time-to-first-chunk streaming. |
| **MOS sample** | Single listener; Arabic MOS is naturalness/clone only (no native Arabic judgment of pronunciation). |

## What’s still missing / how we’d improve

- **Native Arabic / Hindi listeners** for MOS and pronunciation A/B (especially Arabic).
- **Better Hindi ASR** (e.g. IndicWhisper) + number/script normalization so WER reflects TTS, not Whisper quirks.
- **Language-matched reference clips** (Arabic/Hindi speech from the same speaker) instead of English-only cross-lingual cloning.
- **Streaming** path for Chatterbox/XTTS to measure true time-to-first-audio.
- **Prosody / pace control** on Chatterbox (reduce “too fast” on EN) and glitch-free long Hindi on XTTS.
- Optional stronger Arabic clone compare (e.g. Fish-Speech) if cloning + quality both matter and MMS is too weak on WER.
- **More model compares** if time allowed: e.g. CosyVoice2 / Chatterbox-Turbo for English, Fish-Speech for Arabic cloning, and other Indic TTS options beyond Parler — same locked sentences and metrics, to strengthen the “best available right now” claim.
- Product shape: a small **router** service (lang detect → Chatterbox | XTTS) with per-env workers to avoid pip conflicts.

## Closed / third-party tooling disclosure

- Speech generation: **open-source only** (Coqui XTTS, Resemble Chatterbox, AI4Bharat Indic Parler, Meta MMS).
- Evaluation: **openai-whisper**, **Resemblyzer**, **jiwer** (open). No ElevenLabs / OpenAI TTS / cloud TTS APIs for generation.

## License / cloning note

Reference voice is the author’s own recording. Do not clone third-party voices without consent.
