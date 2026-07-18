"""Language TTS pipelines sharing BaseTTSPipeline."""

from pipelines.arabic import ArabicPipeline, default_arabic_pipeline
from pipelines.arabic_mms import ArabicMmsPipeline, default_arabic_mms_pipeline
from pipelines.base import BaseTTSPipeline, SynthResult
from pipelines.config import load_config, project_root
from pipelines.english import EnglishPipeline, default_english_pipeline
from pipelines.english_chatterbox import (
    EnglishChatterboxPipeline,
    default_english_chatterbox_pipeline,
)
from pipelines.hindi import HindiPipeline, default_hindi_pipeline
from pipelines.hindi_parler import HindiParlerPipeline, default_hindi_parler_pipeline
from pipelines.telugu import TeluguPipeline, default_telugu_pipeline

__all__ = [
    "BaseTTSPipeline",
    "SynthResult",
    "load_config",
    "project_root",
    "EnglishPipeline",
    "EnglishChatterboxPipeline",
    "ArabicPipeline",
    "ArabicMmsPipeline",
    "HindiPipeline",
    "HindiParlerPipeline",
    "TeluguPipeline",
    "default_english_pipeline",
    "default_english_chatterbox_pipeline",
    "default_arabic_pipeline",
    "default_arabic_mms_pipeline",
    "default_hindi_pipeline",
    "default_hindi_parler_pipeline",
    "default_telugu_pipeline",
]
