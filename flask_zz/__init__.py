import os
from . import database
from . import auth
from flask import Flask


def create_app(test_config=None, db=database, auth=auth):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flask_zz.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def home():
        return "Home Works!"

    db.init_app(app)
    app.register_blueprint(auth.blueprint)

    return app
