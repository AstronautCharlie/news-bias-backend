from blueprints.subject_matter_date_range import article_search_bp
from blueprints.healthcheck import healthcheck_bp
import logging

from flask import Flask

def create_app():
    configure_app_logging()

    app = Flask(__name__, instance_relative_config=True)

    app = register_blueprints(app)
    
    return app

def configure_app_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

def register_blueprints(app):
    app.register_blueprint(healthcheck_bp)
    app.register_blueprint(article_search_bp)
    return app
