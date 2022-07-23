import base64
import binascii

import cv2
import numpy as np

from face_encoding.util.response_error import raise_error


class ApiUtil:

    @staticmethod
    def to_numpy(encoded) -> np.ndarray:
        """Convert base64 to numpy.
        Args:
            encoded (str): Base64 encoded string to decode.
        Returns:
            'np.ndarray: An ndimentional array of the input image.
        """
        np_res = None
        np_array = np.frombuffer(base64.b64decode(encoded), np.uint8)
        try:
            np_res = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        except cv2.error:
            raise_error(401)
        return np_res

    @staticmethod
    def is_base64(str_b64):
        """Check if str represents base64 format.
        Args:
            str_b64 (str): String containing base64 code.
        Returns:
            bool: True if input is base64 encoded, raise ValueError otherwise.
        """
        try:
            base64.b64decode(str_b64)
        except binascii.Error:
            raise_error(401)

    def is_valid_request(self, request) -> tuple:
        """Check if the request has the valid parameters and values.
        Args:
            request (Request): Object of the request.
        Returns:
            vector: (np.ndarray) an n dimensional array of the 64 image.
        """
        if not request.is_json:
            raise_error(400)
        result = request.get_json()
        # The request contains the correct parameters?
        if not all(key in result for key in ['b64_image', 'face_locations']):
            raise_error(404)
        # Contains a list?
        if isinstance(result['face_locations'], list) is False:
            raise_error(408)
        # Is valid a location parameters?
        self.__is_valid_location_parameter(result['face_locations'])
        # str represents base64?
        image_np = self.__is_64image(result)  # return an numpy array.
        # ---
        return image_np, result['face_locations']

    def __is_64image(self, result) -> np.ndarray:
        """Check if the image is base64 valid.
        Args:
            result (dic): Dictionary with the requisition data.
        Returns:
            np.ndarray: An n dimensional array of the 64 image.
        """
        self.is_base64(result['b64_image'])
        image_np = self.to_numpy(result['b64_image'])
        # Is valid numpy?
        if image_np is None:
            raise_error(401)
        return image_np

    @staticmethod
    def __is_valid_location_parameter(face_locations):
        # Contains a list?
        if isinstance(face_locations, list) is False:
            raise_error(408)

        for location in face_locations:
            # Location contains a dict?
            if isinstance(location, dict) is False:
                raise_error(409)
            # Location got a correct parameters?
            parameters = ['bottom', 'left', 'right', 'top']
            if not all(key in location for key in parameters):
                raise_error(410)
