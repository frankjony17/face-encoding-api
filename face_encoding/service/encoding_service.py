
import dlib
import face_recognition_models as f_r_m

from face_encoding.util.response_error import raise_error


class EncodingService:

    __fr_model = f_r_m.face_recognition_model_location()

    def __init__(self):
        self.pose_predictor = f_r_m.pose_predictor_five_point_model_location()
        self.face_encoder = dlib.face_recognition_model_v1(self.__fr_model)

    def find_landmarks(self, image, face_locations) -> tuple:
        """Find faces landmarks.
        Args:
            image (np.ndarray): Image.
            face_locations (list): Faces locations
        Returns:
            list of tuple: Facial landmarks (x, y) - coordinates.
        """
        shape_predictor = dlib.shape_predictor(self.pose_predictor)
        full_object_detections = dlib.full_object_detections()
        for detection in face_locations:
            full_object_detections.append(shape_predictor(image, detection))
        return full_object_detections

    def face_encodings(self, image_processed_np, face_locations):
        """Generate image encodings from face landmarks.
        Args:
            image_processed_np (numpy.ndarray): Image.
            face_locations (list): Bounding boxes of each face from image_64.
        Returns:
            numpy.ndarray: Faces encodings.
        """
        # How many times to re-sample the face when calculating encoding.
        # Higher is more accurate, but slower (i.e. 100 is 100x slower).
        # Default is 1.
        num_jitters = 1
        vector_list = None
        face_locations = self.__get_bounding_box(face_locations)
        try:
            landmarks = self.find_landmarks(image_processed_np, face_locations)
            vector_list = self.face_encoder.compute_face_descriptor(
                image_processed_np, landmarks, num_jitters)
        except TypeError as error:
            raise_error(405, error)
        return vector_list

    @staticmethod
    def __get_bounding_box(face_locations) -> list:
        boxes = list()
        for location in face_locations:
            box_rectangle = dlib.rectangle(
                location['left'],
                location['top'],
                location['right'],
                location['bottom']
            )
            boxes.append(box_rectangle)
        return boxes
