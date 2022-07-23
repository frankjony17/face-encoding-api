
from flask import Blueprint, abort, jsonify

error_handler = Blueprint('error_handler', __name__)


error_dict = {
    400: {'detail': 'Bad Request, wrong syntax, '
                    'the request could not be understood by the server.'},
    401: {'detail': 'Bad Request, wrong base64 format.'},
    404: {'detail': 'Bad Request, required parameters missing, parameters '
                    'wasn\'t found.'},
    405: None,
    408: {'detail': 'Bad Request, required value is invalid, the value of the '
                    'face_locations parameter must be a list ([])'},
    409: {'detail': 'Bad Request, required value is invalid, the value of the '
                    'face_locations parameter must be a list that contains '
                    'dictionaries ([{}, {}])'},
    410: {'detail': 'Bad Request, required value from face_locations parameter'
                    ' is invalid, the value of the dictionary contained in'
                    ' the list does not contain the valid keys'},
}


def raise_error(code, msg=None):
    if code > 200:
        if msg is not None:
            error_dict[code] = {'detail': str(msg)}
        abort(code)


def response(code):
    """Return response message according to request type of error.
    Args:
        code (int): Code of error.
    Returns:
        dict or None: Message and reason from request type of error.
    """
    return error_dict.get(code, None)


@error_handler.app_errorhandler(400)
def wrong_syntax(error):
    return jsonify(response(400)), 400


@error_handler.app_errorhandler(401)
def no_face(error):
    return jsonify(response(401)), 400


@error_handler.app_errorhandler(404)
def bad_image(error):
    return jsonify(response(404)), 400


@error_handler.app_errorhandler(405)
def error_500(error):
    return jsonify(response(405)), 500


@error_handler.app_errorhandler(408)
def bad_value_1(error):
    return jsonify(response(408)), 400


@error_handler.app_errorhandler(409)
def bad_value_2(error):
    return jsonify(response(409)), 400


@error_handler.app_errorhandler(410)
def bad_value_3(error):
    return jsonify(response(410)), 400
