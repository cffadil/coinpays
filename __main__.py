"""
Example Application

Usage:
    coinpay [options]

Options:
    -h --help                   Show this screen.
"""
from docopt import docopt
from waitress import serve
from coinpay.app import api_app, cfg

#useGunicorn = True
useGunicorn = False

if useGunicorn:

    from gunicorn.app.base import BaseApplication
    from gunicorn.workers.sync import SyncWorker


    class CustomWorker(SyncWorker):
        def handle_quit(self, sig, frame):
            self.app.application.stop(sig)
            super(CustomWorker, self).handle_quit(sig, frame)

        def run(self):
            self.app.application.start()
            super(CustomWorker, self).run()


    class GunicornApp(BaseApplication):
        """ Custom Gunicorn application

        This allows for us to load gunicorn settings from an external source
        """

        def init(self, parser, opts, args):
            pass

        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super(GunicornApp, self).__init__()

        def load_config(self):
            for key, value in self.options.items():
                self.cfg.set(key.lower(), value)

            self.cfg.set('worker_class', 'coinpay.__main__.CustomWorker')

        def load(self):
            return self.application


def main():
    docopt(__doc__)

    if useGunicorn:
        gunicorn_app = GunicornApp(api_app, cfg.gunicorn)
        gunicorn_app.run()
        return
    api_app.start()
    serve(api_app, listen=cfg.waitress.listen)


if __name__ == '__main__':
    main()
