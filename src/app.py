"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Vehicle
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

### USER OPERATIONS ###
@app.route('/user', methods=['GET'])
def handle_users():
    users = User.query.all()
    response_body = {
        "users": [item.serialize() for item in users]
    }
    return jsonify(response_body), 200


### PLANET OPERATIONS ###
@app.route('/planet', methods=['GET'])
def handle_planets():
    planets = Planet.query.all()
    response_body = {
        "planets": [item.serialize() for item in planets]
    }
    return jsonify(response_body), 200

@app.route('/user/planet/favorite', methods=['POST'])
def fav_planet():
    data = request.get_json()
    user_id = data["user"]
    planet_id = data["planet"]
    user = db.session.get(User, user_id)
    planet = db.session.get(Planet, planet_id)
    user.favorite_planets.append(planet)
    db.session.commit()

    return jsonify({"user": user.serialize()}), 200

### CHARACTER OPERATIONS ###
@app.route('/character', methods=['GET'])
def handle_characters():
    characters = Character.query.all()
    response_body = {
        "characters": [item.serialize() for item in characters]
    }
    return jsonify(response_body), 200

@app.route('/user/character/favorite', methods=['POST'])
def fav_character():
    data = request.get_json()
    user_id = data["user"]
    character_id = data["character"]
    user = db.session.get(User, user_id)
    character = db.session.get(Character, character_id)
    user.favorite_characters.append(character)
    db.session.commit()

    return jsonify({"user": user.serialize()}), 200

### VEHICLE OPERATIONS ###
@app.route('/vehicle', methods=['GET'])
def handle_vehicles():
    vehicles = Vehicle.query.all()
    response_body = {
        "vehicles": [item.serialize() for item in vehicles]
    }
    return jsonify(response_body), 200

@app.route('/user/vehicle/favorite', methods=['POST'])
def fav_vehicle():
    data = request.get_json()
    user_id = data["user"]
    vehicle_id = data["vehicle"]
    user = db.session.get(User, user_id)
    vehicle = db.session.get(Vehicle, vehicle_id)
    user.favorite_vehicles.append(vehicle)
    db.session.commit()

    return jsonify({"user": user.serialize()}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
