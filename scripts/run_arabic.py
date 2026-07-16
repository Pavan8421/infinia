#!/usr/bin/env python3
"""Generate Arabic XTTS-v2 clips for the locked test sentences (Phase 4 step 1)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from eval.latency_rtf import format_timing_row, summarize_timing
from pipelines.arabic import default_arabic_pipeline
from pipelines.config import load_config


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()

    cfg = load_config()
    sentences_path = ROOT / cfg["test_sentences"]["path"]
    items = json.loads(sentences_path.read_text(encoding="utf-8"))["languages"]["arabic"]

    print(f"hardware: {cfg['hardware']['gpu']}")
    print(f"model:    {cfg['models']['xtts_v2']['model_name']}")
    print(f"language: ar (MSA) · cross-lingual clone from reference")
    print(f"sentences: {len(items)}")

    pipe = default_arabic_pipeline(ROOT, device=args.device)
    pipe.load()

    timings: dict = {}
    rows = []
    for item in items:
        uid, text = item["id"], item["text"]
        print(f"\n=== {uid} ===\n{text}")
        result = pipe.synth(text, utterance_id=uid)
        print(format_timing_row(result))
        summary = summarize_timing(result)
        rows.append(summary)
        timings[uid] = {
            "gen_time_sec": result.gen_time_sec,
            "audio_duration_sec": result.audio_duration_sec,
            "rtf": result.rtf,
            "mode": result.mode,
        }

    timings_path = pipe.output_dir / "timings.json"
    timings_path.write_text(json.dumps(timings, indent=2), encoding="utf-8")

    print("\n--- summary ---")
    for r in rows:
        print(
            f"{Path(r['wav_path']).name}: gen={r['gen_time_sec']}s "
            f"dur={r['audio_duration_sec']}s RTF={r['rtf']} "
            f"latency_ok={r['meets_latency_target']} rtf_ok={r['meets_rtf_target']}"
        )
    print(f"\nWrote {len(rows)} wavs under {pipe.output_dir}")
    print(f"Wrote {timings_path}")


if __name__ == "__main__":
    main()
