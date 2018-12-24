import falcon
import os
import aumbry
from pyfiglet import Figlet

from .db.model_manager import DBManager
from .middleware.requireJSON import RequireJSON
from .middleware.auth import Auth
from .middleware.session import SQLAlchemySessionManager
from .middleware.context import ContextMiddleware
from .resources.kiosk import KioskAPI
from .resources.dc import DcAPI
from .resources.user import UserAPI
from .resources.cashier import CashierAPI
from .config import AppConfig


def handle404(req, resp):
    f = Figlet(font='colossal')
    f.width = 125
    resp.status = falcon.HTTP_404
    resp.content_type = falcon.MEDIA_TEXT
    resp.body = f.renderText('C o i n p a y s').encode('utf-8')


class CoinpayAPI(falcon.API):
    def __init__(self, cfg):
        self.mgr = DBManager(cfg.db.connection)
        super(CoinpayAPI, self).__init__(
            middleware=[
                ContextMiddleware(),
                RequireJSON(),
                SQLAlchemySessionManager(self.mgr.DBSession),
                Auth(cfg),
            ]
        )

    def start(self):
        self.mgr.setup()
        api_kiosk = KioskAPI(cfg)
        api_dc = DcAPI(cfg)
        api_user = UserAPI(cfg)
        api_cashier = CashierAPI(cfg)
        self.add_route('/kiosk/{method}', api_kiosk)
        self.add_route('/dc/{method}', api_dc)
        self.add_route('/user/{method}', api_user)
        self.add_route('/cashier/{method}', api_cashier)
        self.add_sink(handle404, '')
        pass

    def stop(self, signal):
        pass


cfg = aumbry.load(
    aumbry.FILE,
    AppConfig,
    {
        'CONFIG_FILE_PATH': os.path.dirname(os.path.realpath(__file__))+'/../config/config.yml'
    }
)

api_app = CoinpayAPI(cfg)
api_app.start()
