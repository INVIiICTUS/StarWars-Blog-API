"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, Favourite
#from models import P

api = Blueprint("api", __name__)

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

@app.route('/person', methods=['GET'])
def get_all_person():
    persons = Person.query.all()
    list_all_person = list(map(lambda person: person.serialize(),persons))
    return jsonify(list_all_person),200

@app.route("/person/<int:person_id>", methods=["GET"])
def get_person(person_id):
    person=Person.query.get(person_id)

    if person==None:
        resp = "This person does not exist"
    else:
        resp =person.serialize()
    
    return jsonify(resp),200

@app.route('/planet', methods=['GET'])
def get_planets_all():
    planets = Planet.query.all()
    list_all_planet = list(map(lambda planet: planet.serialize(),planets))
    return jsonify(list_all_planet),200

@app.route("/planet/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet=Planet.query.get(planet_id)

    if planet==None:
        resp = "This planet does not exist"
    else:
        resp =planet.serialize()
    
    return jsonify(resp),200

@app.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    list_all_users = list(map(lambda user: user.serialize(),users))
    return jsonify(list_all_users),200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user == None:
        resp = "User does not exist"
    else:
        resp = user.serialize()

    return jsonify(resp),200    
   

@app.route("/users/favourites/<int:user_id>", methods=["GET"])
def get_favourites_of_user(user_id):
    favourites = Favourite.query.get(user_id)
    if favourites == None:
        resp = "This user has not favourites"
    else:
        resp = favourites.serialize()

    return jsonify(resp),200  

@app.route("/favourite/planet/<int:planet_id>", methods = ["POST"])
def add_planet_favourite(planet_id):
    body = request.get_json()
    print(body)
    new_planet_favourite = Favourite(user_id=body["user_id"], planet_id=body["planet_id"])
    db.session.add(new_planet_favourite)
    db.session.commit()

    return jsonify("Planet added to favourites"),200

@app.route("/favourite/planet/<int:planet_id>", methods = ["DELETE"])
def delete_planet_favourite(planet_id):
    favourite = Favourite.query.get(planet_id)
    if favourite == None:
        return ("this favourite does not exist"),200
    else:
        db.session.delete(favourite)
        db.session.commit()
        return jsonify("Planet deleted from favourites"),200

@app.route("/favourite/person/<int:person_id>", methods = ["POST"])
def add_person_favourite(person_id):
    body = request.get_json()
    new_person_favourite = Favourite(user_id=body["user_id"], person_id=body["person_id"])
    db.session.add(new_person_favourite)
    db.session.commit()

    return jsonify("Person added to favourites"),200

@app.route("/favourite/person/<int:person_id>", methods = ["DELETE"])
def delete_person_favourite(person_id):
    favourite = Favourite.query.get(person_id)
    if favourite == None:
        return ("this favourite does not exist"),200
    else:
        db.session.delete(favourite)
        db.session.commit()   
        return jsonify("Person deleted from favourites"),200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)