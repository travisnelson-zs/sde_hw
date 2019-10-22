from flask import Flask


def create_app():
    """Initialize the core application"""
    from .models import db
    app = Flask(__name__)
    app.config.from_object('config.Testing_Config')
    db.init_app(app)

    with app.app_context():
        from . import models
        # Include our Routes
        from .site.routes import mod
        from .api.routes import mod
        # Register our Blueprints
        app.register_blueprint(site.routes.mod)
        app.register_blueprint(api.routes.mod, url_prefix='/api')
        return app
