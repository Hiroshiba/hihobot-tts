import json
from io import BytesIO
from logging import getLogger
from typing import List

import librosa
import tornado.escape
import tornado.ioloop
import tornado.web
from tornado_cors import CorsMixin

from hihobot_tts import Synthesizer, Answerer


class TextToContextHandler(CorsMixin, tornado.web.RequestHandler):
    CORS_ORIGIN = '*'
    CORS_HEADERS = 'x-requested-with, content-type'
    CORS_METHODS = 'GET, POST'

    def initialize(self, synthesizer: Synthesizer):
        self.synthesizer = synthesizer

    def _text_to_context(self, text: str):
        context = self.synthesizer.text_to_context(text)

        self.set_header('Content-type', 'application/json')
        self.write(json.dumps(context))

    def get(self):
        text: str = self.get_argument('text')
        self._text_to_context(text)

    def post(self):
        text: str = tornado.escape.json_decode(self.request.body)['text']
        self._text_to_context(text)


class ContextToWaveHandler(CorsMixin, tornado.web.RequestHandler):
    CORS_ORIGIN = '*'
    CORS_HEADERS = 'x-requested-with, content-type'
    CORS_METHODS = 'GET, POST'

    def initialize(self, synthesizer: Synthesizer):
        self.synthesizer = synthesizer

    def _context_to_wave(self, context_list: List[str]):
        context = json.loads(context_list)
        wave = self.synthesizer.context_to_wave(context)

        self.set_header('Content-type', 'audio/wav')

        bio = BytesIO()
        librosa.output.write_wav(bio, y=wave.wave, sr=wave.sampling_rate)
        self.write(bio.getvalue())

    def get(self):
        context = json.dumps(self.get_argument('context'))
        self._context_to_wave(context)

    def post(self):
        context = tornado.escape.json_decode(self.request.body)['context']
        self._context_to_wave(context)


class SynthesizeHandler(CorsMixin, tornado.web.RequestHandler):
    CORS_ORIGIN = '*'
    CORS_HEADERS = 'x-requested-with, content-type'
    CORS_METHODS = 'GET, POST'

    def initialize(self, synthesizer: Synthesizer):
        self.synthesizer = synthesizer

    def _synthesize(self, text: str):
        wave = self.synthesizer.synthesize(text)

        self.set_header('Content-type', 'audio/wav')

        bio = BytesIO()
        librosa.output.write_wav(bio, y=wave.wave, sr=wave.sampling_rate)
        self.write(bio.getvalue())

    def get(self):
        text: str = self.get_argument('text')
        self._synthesize(text)

    def post(self):
        text: str = tornado.escape.json_decode(self.request.body)['text']
        self._synthesize(text)


class AnswerHandler(CorsMixin, tornado.web.RequestHandler):
    CORS_ORIGIN = '*'
    CORS_HEADERS = 'x-requested-with, content-type'
    CORS_METHODS = 'GET, POST'

    def initialize(self, answerer: Answerer, logger=getLogger(__name__)):
        self.answerer = answerer
        self.logger = logger

    def _answer(self, text: str):
        self.logger.info(f'input: {text}')
        answer = self.answerer.answer(text)
        self.logger.info(f'answer: {answer}')
        self.write(answer)

    def get(self):
        text: str = self.get_argument('text')
        self._answer(text)

    def post(self):
        text: str = tornado.escape.json_decode(self.request.body)['text']
        self._answer(text)
