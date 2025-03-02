from decouple import config

DB_URI = config("SQLALCHEMY_DATABASE_URI")
API_POKEMON = config("POKEMON_API_URL")


class Config:
    SQLALCHEMY_DATABASE_URI = DB_URI
    SECRET_KEY = config("SECRET_KEY")
    JWT_SECRET_KEY = config("JWT_SECRET_KEY")
