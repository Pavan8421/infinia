#!/usr/bin/env python3
"""Phase 3 step 4: eval English XTTS clips — WER + speaker similarity + latency/RTF."""

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


def _load_timings(path: Path) -> dict:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", default="cuda")
    parser.add_argument(
        "--resynth",
        action="store_true",
        help="Re-run XTTS to refresh latency/RTF (overwrites wavs)",
    )
    parser.add_argument(
        "--wav-dir",
        type=Path,
        default=None,
        help="Directory of en_*.wav (default: outputs/english/xtts)",
    )
    args = parser.parse_args()

    cfg = load_config()
    ref_wav = ROOT / cfg["reference"]["path"]
    sentences = json.loads(
        (ROOT / cfg["test_sentences"]["path"]).read_text(encoding="utf-8")
    )["languages"]["english"]
    wav_dir = args.wav_dir or (ROOT / "outputs" / "english" / "xtts")
    timings_path = wav_dir / "timings.json"
    timings = _load_timings(timings_path)

    print(f"hardware: {cfg['hardware']['gpu']}")
    print(f"reference: {ref_wav}")
    print(f"wav_dir:   {wav_dir}")
    print(f"asr:       {cfg['eval']['asr']['default']}")
    print(f"similarity: resemblyzer")

    if args.resynth:
        from pipelines.english import default_english_pipeline

        pipe = default_english_pipeline(ROOT, device=args.device)
        pipe.load()
        for item in sentences:
            uid, text = item["id"], item["text"]
            print(f"\n[resynth] {uid}")
            result = pipe.synth(text, utterance_id=uid)
            timings[uid] = {
                "gen_time_sec": result.gen_time_sec,
                "audio_duration_sec": result.audio_duration_sec,
                "rtf": result.rtf,
                "mode": result.mode,
            }
        timings_path.write_text(json.dumps(timings, indent=2), encoding="utf-8")
        print(f"wrote {timings_path}")

    rows = []
    for item in sentences:
        uid = item["id"]
        text = item["text"]
        wav_path = wav_dir / f"{uid}.wav"
        print(f"\n=== {uid} ===\n{text}\n{wav_path}")
        if not wav_path.is_file():
            print(f"MISSING: {wav_path} — run scripts/run_english.py first")
            continue

        t0 = time.perf_counter()
        wer_out = round_trip_wer(wav_path, text, language="en", device=args.device)
        print(f"WER: {wer_out['wer_pct']:.1f}%  hyp={wer_out['hypothesis']!r}  ({time.perf_counter()-t0:.1f}s)")

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
            print(f"latency/RTF: n/a (no timings.json — pass --resynth or run run_english.py)")
        else:
            print(
                f"latency: {gen:.4f}s (batch)  dur={timing.get('audio_duration_sec', dur):.4f}s  "
                f"RTF={rtf:.4f}"
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
            }
        )

    out_json = ROOT / "results" / "english_xtts_eval.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "hardware": cfg["hardware"]["gpu"],
        "model": "xtts_v2",
        "reference": str(ref_wav),
        "clips": rows,
        "averages": {
            "wer_pct": sum(r["wer_pct"] for r in rows) / len(rows) if rows else None,
            "cosine": sum(r["cosine"] for r in rows) / len(rows) if rows else None,
            "rtf": (
                sum(r["rtf"] for r in rows if r["rtf"] is not None)
                / max(1, sum(1 for r in rows if r["rtf"] is not None))
                if any(r["rtf"] is not None for r in rows)
                else None
            ),
        },
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("\n--- summary ---")
    for r in rows:
        rtf_s = f"{r['rtf']:.4f}" if r["rtf"] is not None else "n/a"
        gen_s = f"{r['gen_time_sec']:.4f}s" if r["gen_time_sec"] is not None else "n/a"
        print(
            f"{r['id']}: WER={r['wer_pct']:.1f}%  cosine={r['cosine']:.4f}  "
            f"gen={gen_s}  RTF={rtf_s}"
        )
    avg = payload["averages"]
    print(
        f"AVG: WER={avg['wer_pct']:.1f}%  cosine={avg['cosine']:.4f}  "
        f"RTF={avg['rtf'] if avg['rtf'] is not None else 'n/a'}"
    )
    print(f"\nwrote {out_json}")


if __name__ == "__main__":
    main()
