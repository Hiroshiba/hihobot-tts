from pathlib import Path

from hihobot.hihobot import Hihobot

from hihobot_tts.config import AnswererConfig


class Answerer(object):
    def __init__(self, hihobot: Hihobot):
        self.hihobot = hihobot

    def answer(self, text: str):
        vec = self.hihobot.text_to_vec(text=text)
        return self.hihobot.generate(vec=vec)

    @classmethod
    def load(cls, config: AnswererConfig):
        return cls(
            hihobot=Hihobot(
                model_path=Path(config.model_path),
                model_config=Path(config.model_config),
                char_path=Path(config.char_path),
                doc2vec_model_path=Path(config.doc2vec_model_path),
                max_length=config.max_length,
                sampling_maximum=config.sampling_maximum,
                gpu=config.gpu,
            )
        )
