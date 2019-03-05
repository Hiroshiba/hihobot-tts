from logging import getLogger, StreamHandler
from sys import stdout

import fire
import tornado.escape
import tornado.ioloop
import tornado.web

from hihobot_tts import load_config, Synthesizer, Answerer
from hihobot_tts.handler import TextToContextHandler, ContextToWaveHandler, SynthesizeHandler, AnswerHandler


def run(
        config_path: str,
        port=8000,
        debug=False,
):
    config = load_config(config_path)

    handler = StreamHandler(stdout)
    handler.setLevel('INFO')

    logger = getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel('INFO')

    logger.info('Loading Synthesizer...')
    synthesizer = Synthesizer.load(config.synthesiser)

    logger.info('Loading Answerer...')
    answerer = Answerer.load(config.answerer)

    app = tornado.web.Application([
        (r"/text_to_context", TextToContextHandler, dict(synthesizer=synthesizer)),
        (r"/context_to_wave", ContextToWaveHandler, dict(synthesizer=synthesizer)),
        (r"/synthesize", SynthesizeHandler, dict(synthesizer=synthesizer)),
        (r"/answer", AnswerHandler, dict(answerer=answerer)),
    ], debug=debug)

    logger.info('Running!!')

    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    fire.Fire(run)
