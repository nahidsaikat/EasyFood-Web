from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_assets import Environment
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_session import Session

from easy_food.assets import compile_static_assets


csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
assets = Environment()
sess = Session()


def create_app():
    app = Flask(__name__,
                instance_relative_config=False,
                template_folder="templates",
                static_folder="static")
    if app.config['ENV'] == 'production':
        app.config.from_object('config.ProdConfig')
    elif app.config['ENV'] == 'testing':
        app.config.from_object('config.TestConfig')
    else:
        app.config.from_object('config.DevConfig')
    app.secret_key = "super secret key"
    print(app.config)

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    assets.init_app(app)
    sess.init_app(app)

    with app.app_context():
        from easy_food.urls import register_all_blueprints
        register_all_blueprints(app)

        db.create_all()

        if app.config['FLASK_ENV'] == 'development':
            compile_static_assets(assets)
        return app
