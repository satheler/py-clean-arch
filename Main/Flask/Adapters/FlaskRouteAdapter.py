import json
from http import HTTPStatus

from flask import request

from Presentation.Errors.ValidationError import ValidationError
from Presentation.Errors.BusinessError import BusinessError

from Core.Message import Message
from Contracts import Controller


def adapt_route(controller: Controller) -> str:
    data = {}
    if request.query_string:
        data = {**data, **request.args.to_dict()}

    if request.method == 'POST' and request.data:
        data = {**data, **request.json}

    if request.view_args:
        data = {**data, **request.view_args}

    try:
        message = Message(data)
        response = controller.handle(message)
        return json.dumps(response), HTTPStatus.OK
    except BusinessError as business_error:
        return json.dumps(business_error.to_dict()), HTTPStatus.BAD_REQUEST
    except ValidationError as validation_error:
        return json.dumps(validation_error.to_dict()), HTTPStatus.UNPROCESSABLE_ENTITY
    except BaseException as exception:
        print(exception)
        return json.dumps({'message': 'Internal Server Error'}), HTTPStatus.INTERNAL_SERVER_ERROR
