__version__ = '0.1.0'

import logging.config
import os
from pathlib import Path

import yaml
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint


def get_scheme(swagger_yml):
    try:
        swagger_yml['schemes'] = [os.environ['SCHEMES']]
        logging.getLogger('face-encoding.api').info("SCHEMES > OK")
    except KeyError:
        logging.getLogger('face-encoding.api').info('SCHEMES > not found')


def create_app():
    root_path, path = Path(__file__).parents[0], ''
    app = Flask(__name__)

    if os.path.exists(root_path / 'config'):
        root_path = root_path / 'config'
        # logging configs
        if os.environ.get('MODE') == 'prod':
            print('-----STARTING PRODUCTION APPLICATION-----')
            path = root_path / 'logging_cloud.yaml'
        elif os.environ.get('MODE') == 'dev':
            print('----- STARTING DEVELOPMENT APPLICATION -----')

            if not os.path.exists('/var/log/fksolutions/'):
                print('WARNING: Logging will not work since /var/log/fksolutions/ '
                      'do not exist.')
            else:
                path = root_path / 'logging.yaml'
        print(f'----- PID {os.getpid()} -----')

        if path:
            with open(str(path), 'rt') as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)

        # Creates API docs endpoint from swagger file.
        doc_path = str(root_path / 'swagger.yaml')
        swagger_yml = yaml.safe_load(open(doc_path, 'r'))
        # Get scheme.
        get_scheme(swagger_yml)
        # Register Swagger UI.
        app.register_blueprint(
            get_swaggerui_blueprint('/docs', doc_path, config={
                'spec': swagger_yml}), url_prefix='/docs')
    else:
        print('-----STARTING TESTING APPLICATION-----')

    # Error handler
    from face_encoding.util.response_error import error_handler
    app.register_blueprint(error_handler)
    # Helpers controller
    from face_encoding.util.helpers_controller import helpers
    app.register_blueprint(helpers)
    # Start controller
    from face_encoding.controller.start_controller import start_route
    app.register_blueprint(start_route)
    # Detection controller
    from face_encoding.controller.encoding_controller \
        import encoding_route
    app.register_blueprint(encoding_route)
    # Logger
    logging.getLogger('face-encoding.init').info(
        'Application created, ready to up.')
    return app
