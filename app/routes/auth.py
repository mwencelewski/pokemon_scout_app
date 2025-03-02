from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlmodel import select
from libs.models.users import User, get_session
from passlib.hash import pbkdf2_sha256

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    summary: Register a new user
    description: This endpoint registers a new user by accepting a JSON object with a username and password. It checks if the user already exists and returns an error if so.
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: User registration details
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: The desired username
            password:
              type: string
              description: The desired password
    responses:
      200:
        description: User created successfully
        schema:
          type: object
          properties:
            username:
              type: string
              description: The username of the newly created user
            # Additional user fields can be documented here if needed.
      400:
        description: User already exists or invalid input
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating the reason for failure
    """
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
    """
    User login endpoint
    ---
    tags:
      - Authentication
    summary: Logs a user in and returns a JWT access token
    description: >
      This endpoint authenticates a user by verifying the provided username and password.
      If the credentials are valid, a JWT access token is generated and returned.
      Otherwise, an error message is returned.
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: User login credentials
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: The user's username
            password:
              type: string
              description: The user's password
    responses:
      200:
        description: Login successful, returns JWT access token.
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: JWT access token for authenticated requests.
      401:
        description: Invalid credentials provided.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating that the login credentials are invalid.
    """
    data = request.json
    with get_session() as session:
        user = session.exec(
            select(User).where(User.username == data["username"])
        ).first()
        if user and user.check_password(data["password"]):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token)
        return jsonify(message="Invalid credentials"), 401
