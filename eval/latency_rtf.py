"""Latency and real-time factor helpers. Targets: <2s full clip or <500ms first chunk; RTF ≤ 0.5."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from pipelines.base import SynthResult


def summarize_timing(result: SynthResult) -> dict[str, Any]:
    """Flatten SynthResult timing fields for results tables."""
    out = {
        "wav_path": str(result.wav_path),
        "mode": result.mode,
        "gen_time_sec": round(result.gen_time_sec, 4),
        "audio_duration_sec": round(result.audio_duration_sec, 4),
        "rtf": round(result.rtf, 4),
        "latency_to_first_chunk_sec": result.latency_to_first_chunk_sec,
        "meets_rtf_target": result.rtf <= 0.5,
    }
    if result.mode == "batch":
        out["meets_latency_target"] = result.gen_time_sec < 2.0
    else:
        lat = result.latency_to_first_chunk_sec
        out["meets_latency_target"] = lat is not None and lat < 0.5
    out["meta"] = result.meta
    return out


def format_timing_row(result: SynthResult) -> str:
    s = summarize_timing(result)
    lat = s["latency_to_first_chunk_sec"]
    lat_s = f"{lat:.3f}s" if lat is not None else "n/a"
    return (
        f"{s['wav_path']}: mode={s['mode']} gen={s['gen_time_sec']}s "
        f"dur={s['audio_duration_sec']}s RTF={s['rtf']} first_chunk={lat_s}"
    )


# Re-export for notebooks / scripts that only import this module
__all__ = ["summarize_timing", "format_timing_row", "asdict", "SynthResult"]
