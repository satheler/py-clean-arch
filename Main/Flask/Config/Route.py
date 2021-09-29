from flask import Flask
from flask.views import MethodView


class Route:
    _app: Flask

    def __init__(self, app: Flask) -> None:
        self._app = app

    def register(self, endpoint: str, route: MethodView):
        url = f'/{endpoint}/'
        view_func = route.as_view(endpoint)

        self._app.add_url_rule(
            url,
            defaults={'id': None},
            view_func=view_func,
            methods=['GET', ]
        )

        self._app.add_url_rule(
            url,
            view_func=view_func,
            methods=['POST', ]
        )

        self._app.add_url_rule(
            f'{url}<string:id>',
            view_func=view_func,
            methods=['GET', 'PUT', 'DELETE']
        )
