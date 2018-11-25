from io import BytesIO

import fire
import librosa
import tornado.ioloop
import tornado.web

from tornado_cors import CorsMixin

from hihobot_tts import load_config, Synthesizer, Answerer


class SynthesizeHandler(CorsMixin, tornado.web.RequestHandler):
    CORS_ORIGIN = '*'
    CORS_HEADERS = 'x-requested-with'
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
        text: str = self.get_argument('text')
        self._synthesize(text)


class AnswerHandler(CorsMixin, tornado.web.RequestHandler):
    CORS_ORIGIN = '*'
    CORS_HEADERS = 'x-requested-with'
    CORS_METHODS = 'GET, POST'

    def initialize(self, answerer: Answerer):
        self.answerer = answerer

    def _answer(self, text: str):
        self.write(self.answerer.answer(text))

    def get(self):
        text: str = self.get_argument('text')
        self._answer(text)

    def post(self):
        text: str = self.get_argument('text')
        self._answer(text)


def make_app():
    return


def run(
        config_path: str,
        port=8000,
        debug=False,
):
    config = load_config(config_path)

    print('Loading Synthesizer...')
    synthesizer = Synthesizer.load(config.synthesiser)

    print('Loading Answerer...')
    answerer = Answerer.load(config.answerer)

    app = tornado.web.Application([
        (r"/synthesize", SynthesizeHandler, dict(synthesizer=synthesizer)),
        (r"/answer", AnswerHandler, dict(answerer=answerer)),
    ], debug=debug)

    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    fire.Fire(run)
