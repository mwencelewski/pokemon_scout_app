from flask import Flask
from commons import config
from libs.models.users import SQLModel, create_engine, create_table

# from sqlmodel import SQLModel, create_engine
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)
    create_table()
    jwt = JWTManager(app)
    migrate = Migrate(app, SQLModel)
    from routes.auth import auth_bp
    from routes.pokemon import pokemon_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(pokemon_bp, url_prefix="/scrape")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
