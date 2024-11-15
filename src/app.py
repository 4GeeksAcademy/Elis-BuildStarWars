"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, Vehicles, Favorites
import json

app = Flask(__name__)

admin = Admin(app, name="4Geeks Admin",template_mode="bootstrap3")
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# --------------------------------MÉTODOS GET
@app.route('/user', methods=['GET'])
def get_user():
    all_user = User.query.all()
    result = [element.serialize() for element in all_user]
    response_body = {
        "msg": "Muy bien, obtuviste tus usuarios!",
        "user": result
    }
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    result = [element.serialize() for element in all_planets]
    response_body = {
        "msg": "Muy bien, obtuviste tus planetas!",
        "planets": result
    }
    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    all_characters = Characters.query.all()
    result = [element.serialize() for element in all_characters]
    response_body = {
        "msg": "Muy bien, obtuviste tus personajes!",
        "characters": result
    }
    return jsonify(response_body), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    all_vehicles = Vehicles.query.all()
    result = [element.serialize() for element in all_vehicles]
    response_body = {
        "msg": "Muy bien, obtuviste tus vehículos!",
        "vehicles": result
    }
    return jsonify(response_body), 200

@app.route('/favorites', methods=['GET'])
def get_favorites():
    all_favorites = Favorites.query.all()
    result = [element.serialize() for element in all_favorites]
    response_body = {
        "msg": "Muy bien, obtuviste tus Favoritos!",
        "favorites": result
    }
    return jsonify(response_body), 200

# ------------------------------------------MÉTODOS GET POR ID-
@app.route('/users/<int:users_id>', methods=['GET'])
def get_users_id(users_id):
    un_user = User.query.get(users_id)
    result = un_user.serialize()
    response_body = {"msg": "Usuario recibido", "users": result}
    return jsonify(response_body), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets_id(planets_id):
    un_planet = Planets.query.get(planets_id)
    result = un_planet.serialize()
    response_body = {"msg": "Planeta recibido", "planets": result}
    return jsonify(response_body), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_characters_id(character_id):
    un_character = Characters.query.get(character_id)
    result = un_character.serialize()
    response_body = {"msg": "Personaje recibido", "character": result}
    return jsonify(response_body), 200

@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_vehicles_id(vehicles_id):
    un_vehicle = Vehicles.query.get(vehicles_id)
    result = un_vehicle.serialize()
    response_body = {"msg": "Vehículo recibido", "vehicles": result}
    return jsonify(response_body), 200

# --------------------------------------MÉTODOS POST
@app.route('/users', methods=['POST'])
def create_user():
    data = request.data
    data = json.loads(data)
    new_user = User(name=data["name"], email=data["email"], id=data["id"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize())

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.data
    data = json.loads(data)
    new_planet = Planets(
        id=data["id"], name=data["name"], climate=data["climate"],
        terrain=data["terrain"], description=data["description"], diameter=data["diameter"],
        rotation_period=data["rotation_period"], orbital_period=data["orbital_period"]
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize())

@app.route('/characters', methods=['POST'])
def create_character():
    data = request.data
    data = json.loads(data)
    new_character = Characters(
        id=data["id"], name=data["name"], description=data["description"],
        gender=data["gender"], mass=data["mass"]
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize())

@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.data
    data = json.loads(data)
    new_vehicle = Vehicles(
        id=data["id"], name=data["name"], clase=data["clase"],
        capacidad=data["capacidad"], length=data["length"]
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify(new_vehicle.serialize())

# --------------------------MÉTODOS DELETE
@app.route('/users/<int:users_id>', methods=['DELETE'])
def delete_user(users_id):
    borrar_user = User.query.get(users_id)
    db.session.delete(borrar_user)
    db.session.commit()
    return jsonify(borrar_user.serialize())

@app.route('/planets/<int:planets_id>', methods=['DELETE'])
def delete_planet(planets_id):
    borrar_planet = Planets.query.get(planets_id)
    db.session.delete(borrar_planet)
    db.session.commit()
    return jsonify(borrar_planet.serialize())

@app.route('/characters/<int:characters_id>', methods=['DELETE'])
def delete_character(characters_id):
    borrar_character = Characters.query.get(characters_id)
    db.session.delete(borrar_character)
    db.session.commit()
    return jsonify(borrar_character.serialize())

@app.route('/vehicles/<int:vehicles_id>', methods=['DELETE'])
def delete_vehicle(vehicles_id):
    borrar_vehicle = Vehicles.query.get(vehicles_id)
    db.session.delete(borrar_vehicle)
    db.session.commit()
    return jsonify(borrar_vehicle.serialize())

# -------------------POST DE FAVORITOS
@app.route('/favorite/planets/<int:planets_id>', methods=['POST'])
def favorite_planet(planet_id):
    body_request = request.get_json()
    user_id = body_request.get("user_id", None)
    planet_id = body_request.get("planet_id", None)
    new_planet_favorite = Favorites(user_id=user_id, planet_id=planet_id)
    db.session.add(new_planet_favorite)
    db.session.commit()
    return jsonify(new_planet_favorite.serialize())

@app.route('/favorite/characters/<int:characters_id>', methods=['POST'])
def favorite_character(character_id):
    body_request = request.get_json()
    user_id = body_request.get("user_id", None)
    character_id = body_request.get("character_id", None)  # Corrección aquí
    new_character_favorite = Favorites(user_id=user_id, character_id=character_id)
    db.session.add(new_character_favorite)
    db.session.commit()
    return jsonify(new_character_favorite.serialize())

@app.route('/favorite/vehicles/<int:vehicles_id>', methods=['POST'])
def favorite_vehicle(vehicle_id):
    body_request = request.get_json()
    user_id = body_request.get("user_id", None)
    vehicle_id = body_request.get("vehicle_id", None)  # Corrección aquí
    new_vehicle_favorite = Favorites(user_id=user_id, vehicle_id=vehicle_id)
    db.session.add(new_vehicle_favorite)
    db.session.commit()
    return jsonify(new_vehicle_favorite.serialize())

# ------------------------DELETE FAVORITES
@app.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    borrar_planet_fav = Favorites.query.get(planet_id)
    db.session.delete(borrar_planet_fav)
    db.session.commit()
    return jsonify(borrar_planet_fav.serialize())

@app.route('/favorite/characters/<int:character_id>', methods=['DELETE'])
def delete_fav_character(character_id):
    borrar_character_fav = Favorites.query.get(character_id)
    db.session.delete(borrar_character_fav)
    db.session.commit()
    return jsonify(borrar_character_fav.serialize())

@app.route('/favorite/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_fav_vehicle(vehicle_id):
    borrar_vehicle_fav = Favorites.query.get(vehicle_id)
    db.session.delete(borrar_vehicle_fav)
    db.session.commit()
    return jsonify(borrar_vehicle_fav.serialize())

admin.add_views(ModelView(ModelView,db.session))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
