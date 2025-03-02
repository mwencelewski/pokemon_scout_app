from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlmodel import select
from libs.models.users import User, get_session
from passlib.hash import pbkdf2_sha256

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    with get_session() as session:
        user = User(username=username, password=pbkdf2_sha256.hash(password))
        exists = session.exec(select(User).where(User.username == username)).first()
        if exists:
            return jsonify(message="User already exists"), 400
        session.add(user)
        session.commit()
        return jsonify(user.dict())


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    with get_session() as session:
        user = session.exec(
            select(User).where(User.username == data["username"])
        ).first()
        if user and user.check_password(data["password"]):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token)
        return jsonify(message="Invalid credentials"), 401


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
