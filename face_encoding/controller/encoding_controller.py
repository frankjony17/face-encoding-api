import json
import logging

from flask import Blueprint, jsonify, request

from face_encoding.service.encoding_service import EncodingService
from face_encoding.util.api_util import ApiUtil

encoding_route = Blueprint('encoding_route', __name__)


@encoding_route.route("/image/face-encoding", methods=['POST'])
def image_encoding():
    api_util = ApiUtil()
    service = EncodingService()

    image_np, face_locations = api_util.is_valid_request(request)
    faces_encoding = service.face_encodings(image_np, face_locations)
    # Output response.
    output_response = {
        'faces_encoding': json.dumps([
            list(encoding) for encoding in faces_encoding])
    }
    logging.getLogger('encoding.controller').info('face encoding -> OK')
    return jsonify(output_response), 200
