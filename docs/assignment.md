
# Case Study: Multilingual Voice AI Pipeline (English, Arabic, Indian Languages)

Company: Infinia
Role: LLMOps Voice Engineer / Partner (trial task)
Format: Take-home. You figure it out. You pick the models, the tools, and the approach.
Suggested effort: 6 to 10 focused hours, spread over up to 5 days.
Submission: Reply to this email with your work attached. Details in section 7.

---

## 1. Why we're doing this

We'd rather see how you work than read another resume. This task is a small, real slice of what we build. We want to watch how you evaluate open-source models, how you make trade-offs, and how quickly you can get a voice pipeline running that actually sounds human across some very different languages.

So treat it like a mini project that's yours. Choose the tools, make the calls, and tell us why you made them. There are no trick questions here.

This is deliberately the same kind of work you'd do day to day as an LLMOps Voice Engineer at Infinia, so we're using it to simulate the real thing.

One honest ask: we want actual work, not AI slop. Use AI assistants all you like, that's expected. But we can tell the difference between a pipeline you actually built, ran, and benchmarked, and a nice-looking write-up that was generated and never touched real audio. If it becomes clear the work wasn't genuinely done, that's a rejection, and we'd both rather not get there. Show us the runs, the numbers, the clips, the messy parts. That's what we're hiring for.

---

## 2. What we want you to build

Build voice pipelines that turn text into natural, human-sounding speech in three languages:

1. English
2. Arabic (Modern Standard Arabic is fine, a dialect is a nice bonus)
3. An Indian language (Hindi at a minimum, more Indic languages is a bonus)

We want a separate working pipeline for each of the three voices, so three pipelines in total. They can share code and structure, but each language needs to actually run and produce speech. If you end up routing each language to a different model because that's what works best, that's a good answer, just show us the reasoning.

The core generation has to come from open-source models. No closed APIs (ElevenLabs, OpenAI, Google, Azure, and so on) for the actual speech generation. You can use closed tools for side tasks like evaluation, but you have to tell us where.

The question we really want you to answer:

> Which open-source pipeline gives you the most human-like voice with the fastest response, in each of the three languages, and why?

We expect you to search around, try a few models, compare them, and then recommend a winner with evidence behind it. Concretely, we want you to run evals and benchmark each of the three pipelines against the metrics below, tell us which open-source model is genuinely the best available for each language right now, and then be honest about what's still missing and how you would improve it.

---

## 3. What "good" sounds like: the metrics

Whatever you submit, we want to see it measured against these. The numbers matter, and so does the listening test.

1. Naturalness (MOS): Mean Opinion Score, 1 to 5, from real listeners (you plus a few others). How human does it sound? Target: 4.0 / 5 or higher per language.
2. Speaker similarity (cloning): How close the cloned voice is to the reference speaker. Report speaker-embedding cosine similarity plus a human A/B judgment. Target: 0.75 cosine or higher, or clearly "same speaker" to listeners.
3. Latency to first audio: Time to first audio chunk (streaming) or full clip (batch) for a roughly 10-word sentence, on the hardware you name. Target: Under 500 ms to first chunk (streaming), or under 2 s full clip.
4. Real-time factor (RTF): Generation time divided by audio length. Below 1.0 means faster than real time. Target: 0.5 or lower.
5. Intelligibility (round-trip WER): Run your generated audio back through an ASR model and compare the transcript to your input text. Target: 10% or lower per language.
6. Holds up across languages: Does quality stay strong in Arabic and the Indic language, not just English? Target: No language falls below the bars above.

Feel free to add metrics you think matter, like prosody, emotion control, how it handles names and numbers, or GPU cost. We'll give credit for thoughtful additions.

---

## 4. Where you might start (hints, not rules)

Ignore all of this if you want. It's here so you don't burn time hunting for names. The real work is in comparing and integrating, not in discovery.

Multilingual and cloning TTS: XTTS-v2 (Coqui), Fish-Speech, CosyVoice2 (strong streaming latency), IndexTTS-2 (emotion control), Chatterbox and Chatterbox-Turbo (fast, strong in English), OpenVoice, Bark.

Indian languages: AI4Bharat Indic Parler-TTS and Indic-TTS (13 Indic languages including Hindi), plus the Sarvam and Bhashini ecosystem.

Arabic: Check XTTS-v2 and Fish-Speech Arabic coverage, look for Arabic fine-tunes on Hugging Face, and consider Meta's MMS-TTS for breadth.

ASR (for your round-trip WER and any voice-agent framing): Whisper large-v3 or faster-whisper, and IndicWhisper for Indic languages.

Speaker similarity scoring: any speaker-verification or embedding model to compute cosine similarity.

Heads up from our own poking around: the fastest, most natural models right now (CosyVoice2, Chatterbox, IndexTTS-2) mostly don't cover Arabic or Hindi well. So one model for all three probably won't win. A per-language router usually does. If that's where you land, just say so and back it up.

---

## 5. Deliverables: pick one track

Track A, Code
A repo or zip that runs. Include the pipelines, a README with setup and reproduction steps, sample outputs, and a results table against section 3. Even on the code track, you still have to include the evaluation benchmark. We don't want to guess whether it hit the numbers, we want to see them.

Track B, Audio
A set of generated clips covering all three languages, plus the reference clips you cloned from. Add a short notes file mapping each clip to the model and config that made it, along with the measured metrics.

Track C, Written doc
A 2 to 5 page write-up of the pipelines you built, the models you compared, and the results. If you go this route, the reported metrics have to actually meet the section 3 targets and be reproducible from what you describe. Give enough config detail (model versions, hardware, parameters) that we could rebuild it.

Every track needs:
- Evals and benchmark numbers for each of the three pipelines, against the section 3 metrics, regardless of track
- The models you tested and why the winner won (a comparison table beats paragraphs)
- A clear call on the best available open-source model for each language right now, based on your benchmarks
- Your recommended pipeline for each language and the reasoning behind it
- Where it breaks. Honest failure modes: a specific language, long text, names, whatever tripped it up
- What's still missing in the open-source options and how you would improve it if this were your project

---

## 6. Ground rules

- Open-source models for the core generation. Disclose anything closed you used for tooling or evaluation.
- Reproducibility: name your model versions, hardware, and key parameters.
- For voice cloning, use your own voice or an openly licensed sample. Please don't clone a real person without their consent.
- Be honest about the limits. We'd much rather read "this didn't work and here's why" than see inflated numbers.
- Using AI coding assistants is fine and expected.

---

## 7. How to submit

Reply directly to this email with your work attached (or a link to a repo or Drive folder if it's large). Put a one-paragraph summary of your recommended setup at the top of whatever you send.

If you hit an ambiguity, make a call, state your assumption in the submission, and keep going. Being comfortable with ambiguity is part of what we're looking at.

---