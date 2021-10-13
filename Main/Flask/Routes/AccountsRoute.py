import logging
from flask.views import MethodView

from Main.Flask.Adapters.FlaskRouteAdapter import adapt_route
from Main.Factories.Account.SignUpControllerFactory import make_sign_up_controller

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class AccountsRoute(MethodView):
    def post(self):
        return adapt_route(make_sign_up_controller())
