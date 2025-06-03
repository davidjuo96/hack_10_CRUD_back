import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from .models import User
from .db import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://hack-10-crud-front.vercel.app"]}})

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def index():
    return "Conectado a la base de datos en AWS"

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id, "name": u.name, "email": u.email, "age": u.age
    } for u in users])

@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    new_user = User(
        id=str(uuid.uuid4()),
        name=data["name"],
        email=data["email"],
        age=data["age"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuario creado"}), 201

@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    user.name = data["name"]
    user.email = data["email"]
    user.age = data["age"]
    db.session.commit()
    return jsonify({"message": "Usuario actualizado"})

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"})
