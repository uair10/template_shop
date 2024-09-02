from flask import Flask, g, request
from flask_babelex import Babel
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from template_shop.core.config import DbConfig
from template_shop.core.logger import configure_logging
from template_shop.infrastructure.config_loader import load_config
from template_shop.infrastructure.database.models import BaseModel

db = SQLAlchemy(metadata=BaseModel.metadata)
login_manager = LoginManager()
babel = Babel()


def create_app():
    config = load_config(DbConfig, "db")
    configure_logging()

    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.full_url(with_driver=False)

    from template_shop.admin_panel import config

    app.config.from_object(config.ProdConfig)
    db.init_app(app)

    login_manager.init_app(app)
    babel.init_app(app)

    with app.app_context():
        from . import auth, media
        from .admin import init_admin_panel

        @babel.localeselector
        def get_locale():
            if "favicon" not in request.path:
                if not g.get("lang_code", None):
                    g.lang_code = (
                        request.accept_languages.best_match(app.config["LANGUAGES"]) or app.config["LANGUAGES"][0]
                    )
                return g.lang_code
            return None

        init_admin_panel(app)

        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(media.media_bp)

        return app
