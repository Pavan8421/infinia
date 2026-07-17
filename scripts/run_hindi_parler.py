#!/usr/bin/env python3
"""Generate Hindi Indic Parler-TTS clips for the locked test sentences."""

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
from pipelines.hindi_parler import DEFAULT_DESCRIPTION, default_hindi_parler_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", default="cuda")
    parser.add_argument(
        "--description",
        default=None,
        help="Speaker/style description (default: Divya from model card)",
    )
    args = parser.parse_args()

    cfg = load_config()
    parler_cfg = cfg.get("models", {}).get("indic_parler_tts", {})
    description = args.description or parler_cfg.get(
        "default_description", DEFAULT_DESCRIPTION
    )
    sentences_path = ROOT / cfg["test_sentences"]["path"]
    items = json.loads(sentences_path.read_text(encoding="utf-8"))["languages"]["hindi"]

    print(f"hardware: {cfg['hardware']['gpu']}")
    print(f"model:    {parler_cfg.get('model_name')}")
    print(f"language: hi · description/style (NOT wav cloning)")
    print(f"description: {description}")
    print(f"sentences: {len(items)}")

    pipe = default_hindi_parler_pipeline(
        ROOT, device=args.device, description=description
    )
    pipe.load()

    timings: dict = {}
    rows = []
    for item in items:
        uid, text = item["id"], item["text"]
        print(f"\n=== {uid} ===\n{text}")
        result = pipe.synth(text, utterance_id=uid)
        result.meta["description"] = description
        result.meta["cloning"] = False
        print(format_timing_row(result))
        summary = summarize_timing(result)
        rows.append(summary)
        timings[uid] = {
            "gen_time_sec": result.gen_time_sec,
            "audio_duration_sec": result.audio_duration_sec,
            "rtf": result.rtf,
            "mode": result.mode,
            "description": description,
        }

    timings_path = pipe.output_dir / "timings.json"
    timings_path.write_text(
        json.dumps(timings, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print("\n--- summary ---")
    for r in rows:
        print(
            f"{Path(r['wav_path']).name}: gen={r['gen_time_sec']}s "
            f"dur={r['audio_duration_sec']}s RTF={r['rtf']} "
            f"latency_ok={r['meets_latency_target']} rtf_ok={r['meets_rtf_target']}"
        )
    print(f"\nWrote {len(rows)} wavs under {pipe.output_dir}")
    print(f"Wrote {timings_path}")
    print(
        "\nNote: speaker similarity vs reference WAV will likely be low — "
        "Parler does not clone; it uses a named-speaker description."
    )


if __name__ == "__main__":
    main()
