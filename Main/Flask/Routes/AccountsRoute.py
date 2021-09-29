from flask.views import MethodView


class AccountsRoute(MethodView):
    def post(self):
        # create a new user
        return '{}'
