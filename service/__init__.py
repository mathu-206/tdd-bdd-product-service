"""Flask application package"""
from flask import Flask
from service import config
from service.models import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.app_context():
    from service import routes  # noqa: F401, E402
    from service.common import error_handlers  # noqa: F401, E402

    db.create_all()

app.logger.info("Product service ready")
