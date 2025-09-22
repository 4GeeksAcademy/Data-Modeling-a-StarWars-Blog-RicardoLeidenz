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

##########################
##   USER OPERATIONS    ##
##########################


@app.route('/user', methods=['GET'])
def handle_users():
    users = User.query.all()
    response_body = {
        "users": [item.serialize() for item in users]
    }
    return jsonify(response_body), 200


@app.route('/user', methods=['POST'])
def add_user():
    new_user = request.get_json()
    # Check if all information was provided
    if "email" in new_user:
        new_user = User(email=new_user["email"])
        db.session.add(new_user)
        db.session.commit()
        return {"New User added": new_user.serialize()}, 201
    else:
        return {"Error": "Wrong information submitted"}, 400


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_to_delete = db.session.get(User, user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return {"User deleted": user_to_delete.serialize()}, 200
    else:
        return {"Error": "Incorrect id submitted"}, 400

###### USER FAVORITES OPERATIONS ######


@app.route('/user/favorite/planet', methods=['POST'])
def favorite_planet():
    data = request.get_json()
    user_id = data["user"]
    planet_id = data["planet"]
    user = db.session.get(User, user_id)
    planet = db.session.get(Planet, planet_id)
    user.favorite_planets.append(planet)
    db.session.commit()
    return jsonify({"user": user.serialize()}), 200


@app.route('/user/favorite/character', methods=['POST'])
def favorite_character():
    data = request.get_json()
    user_id = data["user"]
    character_id = data["character"]
    user = db.session.get(User, user_id)
    character = db.session.get(Character, character_id)
    user.favorite_characters.append(character)
    db.session.commit()
    return jsonify({"user": user.serialize()}), 200


@app.route('/user/favorite/vehicle', methods=['POST'])
def favorite_vehicle():
    data = request.get_json()
    user_id = data["user"]
    vehicle_id = data["vehicle"]
    user = db.session.get(User, user_id)
    vehicle = db.session.get(Vehicle, vehicle_id)
    user.favorite_vehicles.append(vehicle)
    db.session.commit()
    return jsonify({"user": user.serialize()}), 200


##########################
##   PLANET OPERATIONS  ##
##########################

@app.route('/planet', methods=['GET'])
def handle_planets():
    planets = Planet.query.all()
    response_body = {
        "planets": [item.serialize() for item in planets]
    }
    return jsonify(response_body), 200


@app.route('/planet', methods=['POST'])
def add_planet():
    new_planet = request.get_json()
    # Check if all information was provided
    if "name" in new_planet:
        new_planet = Planet(email=new_planet["email"])
        db.session.add(new_planet)
        db.session.commit()
        return {"New User added": new_planet.serialize()}, 201
    else:
        return {"Error": "Wrong information submitted"}, 400


@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet_to_delete = db.session.get(Planet, planet_id)
    if planet_to_delete:
        db.session.delete(planet_to_delete)
        db.session.commit()
        return {"Planet deleted": planet_to_delete.serialize()}, 200
    else:
        return {"Error": "Incorrect id submitted"}, 400

##########################
## CHARACTER OPERATIONS ##
##########################


@app.route('/character', methods=['GET'])
def handle_characters():
    characters = Character.query.all()
    response_body = {
        "characters": [item.serialize() for item in characters]
    }
    return jsonify(response_body), 200


@app.route('/character', methods=['POST'])
def add_character():
    new_character = request.get_json()
    # Check if all information was provided
    if "name" in new_character:
        new_character = Character(name=new_character["name"])
        db.session.add(new_character)
        db.session.commit()
        return {"New User added": new_character.serialize()}, 201
    else:
        return {"Error": "Wrong information submitted"}, 400


@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character_to_delete = db.session.get(Character, character_id)
    if character_to_delete:
        db.session.delete(character_to_delete)
        db.session.commit()
        return {"Character deleted": character_to_delete.serialize()}, 200
    else:
        return {"Error": "Incorrect id submitted"}, 400

##########################
### VEHICLE OPERATIONS ###
##########################


@app.route('/vehicle', methods=['GET'])
def handle_vehicles():
    vehicles = Vehicle.query.all()
    response_body = {
        "vehicles": [item.serialize() for item in vehicles]
    }
    return jsonify(response_body), 200


@app.route('/vehicle', methods=['POST'])
def add_vehicle():
    new_vehicle = request.get_json()
    # Check if all information was provided
    if "name" in new_vehicle:
        new_vehicle = Vehicle(email=new_vehicle["name"])
        db.session.add(new_vehicle)
        db.session.commit()
        return {"New User added": new_vehicle.serialize()}, 201
    else:
        return {"Error": "Wrong information submitted"}, 400


@app.route('/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle_to_delete = db.session.get(Vehicle, vehicle_id)
    if vehicle_to_delete:
        db.session.delete(vehicle_to_delete)
        db.session.commit()
        return {"Vehicle deleted": vehicle_to_delete.serialize()}, 200
    else:
        return {"Error": "Incorrect id submitted"}, 400


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
