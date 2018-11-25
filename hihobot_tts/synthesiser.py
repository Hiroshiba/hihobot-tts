from pathlib import Path
from typing import List

import pyopenjtalk
from hihobot_synthesis import load_from_json, Synthesizer as _Synthesizer
from hihobot_synthesis.wave import Wave
from nnmnkwii.io import hts

from hihobot_tts.config import SynthesizerConfig


class Synthesizer(object):
    def __init__(self, synthesizer):
        self.synthesizer = synthesizer

    def text_to_context(self, text: str) -> List[str]:
        label_list = pyopenjtalk.run_frontend(text)[1]
        return label_list

    def context_to_wave(self, label: List[str]):
        return self.synthesizer.test_one_utt(label)

    def synthesize(self, text: str) -> Wave:
        lines = self.text_to_context(text)
        context = hts.load(lines=[l + ' ' for l in lines])  # TODO: should remove this magic
        wave = self.context_to_wave(context)
        return wave

    @classmethod
    def load(cls, config: SynthesizerConfig):
        return cls(
            synthesizer=_Synthesizer(
                config=load_from_json(Path(config.config_path)),
                duration_model_path=Path(config.duration_model_path),
                acoustic_model_path=Path(config.acoustic_model_path),
            )
        )
