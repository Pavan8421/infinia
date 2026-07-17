#!/usr/bin/env python3
"""Eval Hindi Indic Parler clips — WER + speaker similarity + latency/RTF."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from eval.similarity import speaker_similarity
from eval.wer import round_trip_wer
from pipelines.config import load_config


def _audio_duration(wav_path: Path) -> float:
    info = sf.info(str(wav_path))
    return float(info.frames) / float(info.samplerate)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--wav-dir", type=Path, default=None)
    args = parser.parse_args()

    cfg = load_config()
    ref_wav = ROOT / cfg["reference"]["path"]
    sentences = json.loads(
        (ROOT / cfg["test_sentences"]["path"]).read_text(encoding="utf-8")
    )["languages"]["hindi"]
    wav_dir = args.wav_dir or (ROOT / "outputs" / "hindi" / "parler")
    timings_path = wav_dir / "timings.json"
    timings = (
        json.loads(timings_path.read_text(encoding="utf-8"))
        if timings_path.is_file()
        else {}
    )

    print(f"hardware: {cfg['hardware']['gpu']}")
    print(f"reference: {ref_wav}")
    print(f"wav_dir:   {wav_dir}")
    print(f"asr language: hi")
    print("note: Parler is description-based — cosine vs ref WAV is informational")

    rows = []
    for item in sentences:
        uid, text = item["id"], item["text"]
        wav_path = wav_dir / f"{uid}.wav"
        print(f"\n=== {uid} ===\n{text}\n{wav_path}")
        if not wav_path.is_file():
            print("MISSING — run scripts/run_hindi_parler.py first")
            continue

        t0 = time.perf_counter()
        wer_out = round_trip_wer(wav_path, text, language="hi", device=args.device)
        print(
            f"WER: {wer_out['wer_pct']:.1f}%  hyp={wer_out['hypothesis']!r}  "
            f"({time.perf_counter()-t0:.1f}s)"
        )

        sim_out = speaker_similarity(ref_wav, wav_path, device=args.device)
        print(
            f"similarity cosine: {sim_out['cosine']:.4f} "
            f"(target>=0.75: {sim_out['meets_target']})"
        )

        dur = _audio_duration(wav_path)
        timing = timings.get(uid, {})
        gen = timing.get("gen_time_sec")
        rtf = timing.get("rtf")
        if gen is None:
            print("latency/RTF: n/a")
        else:
            print(
                f"latency: {gen:.4f}s (batch)  "
                f"dur={timing.get('audio_duration_sec', dur):.4f}s  RTF={rtf:.4f}"
            )

        rows.append(
            {
                "id": uid,
                "text": text,
                "wav_path": str(wav_path),
                "wer_pct": wer_out["wer_pct"],
                "hypothesis": wer_out["hypothesis"],
                "cosine": sim_out["cosine"],
                "cosine_meets_target": sim_out["meets_target"],
                "gen_time_sec": gen,
                "audio_duration_sec": timing.get("audio_duration_sec", dur),
                "rtf": rtf,
                "description": timing.get("description"),
            }
        )

    out_json = ROOT / "results" / "hindi_parler_eval.json"
    avg_wer = sum(r["wer_pct"] for r in rows) / len(rows) if rows else None
    avg_cos = sum(r["cosine"] for r in rows) / len(rows) if rows else None
    rtf_vals = [r["rtf"] for r in rows if r["rtf"] is not None]
    payload = {
        "hardware": cfg["hardware"]["gpu"],
        "model": "indic_parler_tts",
        "language": "hindi",
        "reference": str(ref_wav),
        "cloning": False,
        "cloning_note": (
            "Description/named-speaker control only; not WAV cloning. "
            "Speaker cosine vs assignment reference is expected to be low."
        ),
        "clips": rows,
        "averages": {
            "wer_pct": avg_wer,
            "cosine": avg_cos,
            "rtf": sum(rtf_vals) / len(rtf_vals) if rtf_vals else None,
        },
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print("\n--- summary ---")
    for r in rows:
        rtf_s = f"{r['rtf']:.4f}" if r["rtf"] is not None else "n/a"
        print(
            f"{r['id']}: WER={r['wer_pct']:.1f}%  cosine={r['cosine']:.4f}  RTF={rtf_s}"
        )
    if rows:
        print(
            f"AVG: WER={avg_wer:.1f}%  cosine={avg_cos:.4f}  "
            f"RTF={payload['averages']['rtf']}"
        )
    print(f"\nwrote {out_json}")


if __name__ == "__main__":
    main()
