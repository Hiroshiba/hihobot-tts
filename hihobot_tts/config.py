import json
from typing import NamedTuple


class AnswererConfig(NamedTuple):
    model_path: str
    model_config: str
    char_path: str
    doc2vec_model_path: str
    max_length: int
    sampling_maximum: bool
    gpu: int


class SynthesizerConfig(NamedTuple):
    config_path: str
    duration_model_path: str
    acoustic_model_path: str


class Config(NamedTuple):
    answerer: AnswererConfig
    synthesiser: SynthesizerConfig


def load_config(path: str):
    d = json.load(open(path))
    return Config(
        answerer=AnswererConfig(**d['answerer']),
        synthesiser=SynthesizerConfig(**d['synthesiser']),
    )
