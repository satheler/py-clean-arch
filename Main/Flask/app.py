from flask import Flask

from Main.Flask.Config.Route import Route
from Main.Flask.Routes.AccountsRoute import AccountsRoute

app = Flask(__name__)

router = Route(app)
router.register('accounts', AccountsRoute)
