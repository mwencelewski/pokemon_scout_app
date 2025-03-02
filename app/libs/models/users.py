from sqlmodel import SQLModel, Field, Session, create_engine
from passlib.hash import pbkdf2_sha256
from contextlib import contextmanager
from commons import config
from pydantic import root_validator
import libs.models.pokemon


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str = Field(alias="password")

    def check_password(self, plain_password: str) -> bool:
        return pbkdf2_sha256.verify(plain_password, self.hashed_password)


engine = create_engine(config.Config.SQLALCHEMY_DATABASE_URI, echo=True)


def create_table():
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    with Session(engine) as session:
        yield session
