# Track A Plan — Multilingual Voice AI Pipeline

**Assignment:** Build three open-source TTS pipelines (English, Arabic, Hindi) that clone a voice, sound natural, and are benchmarked against Section 3 metrics.

**Track:** A (Code) — runnable repo + README + sample outputs + results table + evals.

**Repo:** `infinia/` (Lightning Studio). Telugu is **out of scope**.

**Core constraint:** Speech generation = open-source only. Closed tools OK for evaluation only (disclose if used).

---

## Target metrics (Section 3)

| Metric | Target |
|--------|--------|
| Naturalness (MOS) | ≥ 4.0 / 5 |
| Speaker similarity (cosine) | ≥ 0.75 |
| Latency | < 500 ms first chunk (stream) or < 2 s full clip (batch) |
| Real-time factor (RTF) | ≤ 0.5 |
| Round-trip WER (via ASR) | ≤ 10% |
| Cross-language consistency | EN, AR, HI all meet the above |

---

## Locked decisions

| Item | Choice |
|------|--------|
| Hardware | NVIDIA RTX PRO 6000 Blackwell Server Edition (96 GB) on Lightning AI |
| Languages | English, Arabic (MSA), Hindi only — **no Telugu** |
| Reference | Own voice → `data/reference/speaker_ref.wav` (must restore after fresh clone) |
| Test set | Locked in `data/test_sentences.json` (3 sentences/lang; one with name+number) |
| Env | Single Lightning `cloudspace` venv (no per-model conda). Conflict → second Studio, same GPU named in results |
| Eval stack | Whisper large-v3 (WER), Resemblyzer (speaker sim), batch latency + RTF |

---

## Current status (as of clone)

### Done

| Area | What’s in place |
|------|-----------------|
| Scaffold | `pipelines/`, `eval/`, `scripts/`, `configs/models.yaml`, requirements |
| English XTTS-v2 | Pipeline + run/eval scripts; prior metrics: sim 0.79, RTF 0.21, WER 0%, latency OK |
| Arabic XTTS-v2 | Pipeline + run/eval; prior: sim 0.81, RTF 0.22, latency OK; **WER 23.8% ✗** |
| Hindi XTTS-v2 | Pipeline + run/eval; prior: sim 0.86, RTF 0.21, latency OK; **WER 50% ✗** |
| Auto eval harness | WER / cosine / latency-RTF scripts for all three languages |
| Results | `results/results_table.md` + `*_xtts_eval.json` from prior Studio run |

### Blockers on this Studio (do before new benchmarks)

1. Restore `data/reference/speaker_ref.wav` (missing from clone).
2. Install deps: `requirements/base.txt` → `xtts.txt` → `eval.txt` (CPU OK).
3. Enable GPU, then regenerate WAVs (`scripts/run_{english,arabic,hindi}.py`) — outputs are gitignored.
4. Re-run evals so paths/numbers match this machine.

### Not done (assignment gaps — **priority work**)

| Gap | Why it matters |
|-----|----------------|
| **≥2 models per language, compared** | Assignment asks which OSS pipeline wins *with evidence*; XTTS-only is incomplete |
| **MOS scores** | Required metric; `eval/mos_sheet.csv` is empty |
| **Winners per language** | Explicit call + comparison table |
| **Failure modes + “what’s missing”** | Required in every track |
| **README package** | Reproduce steps, one-paragraph recommended setup, curated samples |
| **WER on AR/HI** | Above target — listen, fix ASR normalization, and/or better models |
| **Streaming latency** | Optional if batch &lt;2s is reported honestly (current approach is batch) |

---

## Remaining phases (focus: multi-model compare)

### Phase A — Studio restore (short)

1. Restore reference WAV.
2. `pip install` base + xtts + eval.
3. Turn on GPU → regenerate XTTS clips → re-eval EN/AR/HI.
4. Spot-listen clips; note ASR vs TTS errors for AR/HI WER.

**Done when:** fresh WAVs + eval JSONs on this Studio; results table updated for XTTS baseline.

---

### Phase B — Try alternate models & compare (main work)

Same locked sentences + same metrics for every model×language. Prefer models that can clone (or note if style-only).

| Language | Baseline (have) | Compare next (pick ≥1 each) | Fallback if deps break |
|----------|-----------------|-----------------------------|------------------------|
| **English** | XTTS-v2 | Chatterbox / CosyVoice2 / Fish-Speech | Piper (no clone; latency only) |
| **Arabic** | XTTS-v2 | Fish-Speech and/or MMS-TTS (Arabic) | Arabic fine-tune on HF if found |
| **Hindi** | XTTS-v2 | **Indic Parler-TTS** (primary compare) | Indic-TTS / MMS Hindi |

**Per model workflow**

1. Add/extend pipeline under `pipelines/` (or model-specific module) + `requirements/*.txt` + `configs/models.yaml` status.
2. `scripts/run_<lang>.py` (or sibling) → `outputs/<lang>/<model>/`.
3. Eval with existing harness → `results/<lang>_<model>_eval.json`.
4. Append row to `results/results_table.md`.
5. Listen: naturalness + “same speaker?” A/B vs reference.

**Done when:** each of EN / AR / HI has **≥2 models** fully measured (auto metrics + notes). Expect a **per-language router**, not one model for all three.

---

### Phase C — Human MOS + WER honesty

1. Fill `eval/mos_sheet.csv`: you + 2–3 listeners, 1–5 per clip (or per language×model average).
2. For AR/HI high WER: listen first; add number/script normalization in `eval/wer.py` if ASR is the culprit; report both raw and normalized if useful.
3. Optional: IndicWhisper for Hindi if Whisper large-v3 is unfair.

**Done when:** MOS column filled for finalists; WER story is credible (TTS vs ASR blame separated).

---

### Phase D — Winners, failures, package (assignment deliverables)

1. **Comparison table** — model×language × all Section 3 metrics vs targets.
2. **Winner per language** — one-line reason tied to numbers (naturalness vs latency trade-off OK).
3. **Failure modes** — long text, names, numbers, cross-lingual clone, Arabic diacritics, Hindi WER, whatever broke.
4. **What’s still missing / how you’d improve** — OSS Arabic/Hindi gaps, streaming, better cloning refs.
5. **README** — setup, hardware, model versions, exact commands; **one-paragraph recommended setup** at top (also for submission email).
6. Curate best sample WAVs per language (winner model) for submission.

**Done when:** a reviewer can reproduce from README and see evidence for each winner.

---

## Suggested time budget (remaining ~6–8 hrs)

| Phase | Focus | Time |
|-------|--------|------|
| A | Restore env + re-baseline XTTS | 0.5–1.0 h |
| B | Alternate models + compare (core) | 3.0–4.0 h |
| C | MOS + WER cleanup | 1.0–1.5 h |
| D | Winners, write-up, README | 1.0–1.5 h |

---

## Assignment checklist (Track A)

- [ ] Three working pipelines (EN, AR, HI) — XTTS done; need second models
- [ ] Open-source generation only; disclose any closed eval tooling
- [ ] Evals for each pipeline vs Section 3 metrics
- [ ] Models tested + **comparison table** + why the winner won
- [ ] Clear best OSS model **per language** right now
- [ ] Recommended pipeline per language + reasoning
- [ ] Honest failure modes
- [ ] What’s missing / how you’d improve
- [ ] README with setup + reproduce steps
- [ ] Sample outputs + results table
- [ ] Reproducibility: model versions, hardware, key params named

---

## Risk notes

- **Dependency conflicts** (XTTS vs Parler/CosyVoice) — sequential install or second Studio; always report RTX PRO 6000.
- **WAVs not in git** — always regenerate after clone.
- **Arabic / Hindi WER** hard to hit 10% with Whisper alone — document ASR limits; don’t inflate numbers.
- **Cloning** — cross-lingual from one English ref; say so; ideally add language-matched refs later if time.
- **Streaming &lt;500 ms** — only claim if you wire streaming; otherwise report batch &lt;2 s honestly.

---

## Immediate next actions

1. ~~Model compares (EN Chatterbox, HI Parler, AR MMS)~~ Done — see `results/results_table.md`.
2. **MOS** — fill `eval/mos_sheet.csv` for finalists (you + 1–2 listeners).
3. **Declare winners** per language in the results table.
4. **Write-up** — failure modes, what’s missing, README one-paragraph recommended setup.
