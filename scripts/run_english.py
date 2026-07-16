#!/usr/bin/env python3
"""Generate English XTTS-v2 clips for the locked test sentences (Phase 2 step 4)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from eval.latency_rtf import format_timing_row, summarize_timing
from pipelines.config import load_config
from pipelines.english import default_english_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--device",
        default="cuda",
        help="Torch device (default: cuda)",
    )
    args = parser.parse_args()

    cfg = load_config()
    sentences_path = ROOT / cfg["test_sentences"]["path"]
    data = json.loads(sentences_path.read_text(encoding="utf-8"))
    items = data["languages"]["english"]

    print(f"hardware: {cfg['hardware']['gpu']}")
    print(f"model:    {cfg['models']['xtts_v2']['model_name']}")
    print(f"sentences: {len(items)} from {sentences_path}")

    pipe = default_english_pipeline(ROOT, device=args.device)
    pipe.load()

    rows = []
    for item in items:
        uid = item["id"]
        text = item["text"]
        print(f"\n=== {uid} ===\n{text}")
        result = pipe.synth(text, utterance_id=uid)
        print(format_timing_row(result))
        rows.append(summarize_timing(result))

    print("\n--- summary ---")
    for r in rows:
        print(
            f"{Path(r['wav_path']).name}: gen={r['gen_time_sec']}s "
            f"dur={r['audio_duration_sec']}s RTF={r['rtf']} "
            f"latency_ok={r['meets_latency_target']} rtf_ok={r['meets_rtf_target']}"
        )
    print(f"\nWrote {len(rows)} wavs under {pipe.output_dir}")


if __name__ == "__main__":
    main()
