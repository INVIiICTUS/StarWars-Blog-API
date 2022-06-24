"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

import email
import json
from ntpath import join
import os
import re
from unicodedata import category
from urllib import response
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import Favorito, Personaje, Planeta, db, Usuario

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('FLASK_APP_KEY')
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users')
def handle_users():
    
    users = Usuario.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200

@app.route('/signup', methods = ['POST'])
def add_user():
    body = request.json
    email_2 = body.get("email", None)
    password = body.get("password", None)
    nombre = body.get("nombre", None)
    apellido = body.get("apellido", None)

    if email_2 and password and nombre is not None:
        correo = Usuario.query.filter_by(email = email_2).first()
        if correo is not None:
            return jsonify({
                "msg": "Usuario ya existe"
            }), 400
        else:
            try:
                new_user = Usuario(
                    email = email_2,
                    password = password,
                    nombre = nombre,
                    apellido = apellido
                )
                db.session.add(new_user)
                db.session.commit()
                return "Usuario creado", 201
            except Exception as error:
                db.session.rollback()
                return jsonify(error.args), 500
    else:
        return jsonify({
            "msg": "Something happened"
        }), 400

@app.route('/login', methods = ['POST'])
def log_in():
    body = request.json
    email_2 = body.get("email", None)
    password = body.get("password", None)

    if email_2 and password is not None:
        correo = Usuario.query.filter_by(email = email_2).first()
        if correo is not None:
            contra = Usuario.query.filter_by(password = password).first()
            if contra is not None:
                token = create_access_token(identity=email_2)
                return jsonify({
                    "email": email_2,
                    "token": token
                }), 200
            else:
                return jsonify({
                    "msg":"Contraseña incorrecta"
                }), 404
        else:
            return jsonify({
                "msg":"Usuario no existe"
            }), 404
    else:
        return jsonify({
            "msg": "Email and Password are necesary"
        }), 401


@app.route('/people')
def handle_people():

    people = Personaje.query.all()
    people = list(map(lambda person: person.serialize(), people))
    return jsonify(people), 200

@app.route('/people/<int:people_id>')
def handle_people_id(people_id):

    person = Personaje.query.filter_by(id = people_id).first()
    if person is not None:
        return jsonify(person.serialize()), 200
    else:
        return jsonify({
            "msg": "Not Found"
        }), 404

@app.route('/planets')
def handle_planets():

    planets = Planeta.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200

@app.route('/planets/<int:planet_id>')
def handle_planets_id(planet_id):

    planet = Planeta.query.filter_by(id= planet_id).first()
    if planet is not None:
        return jsonify(planet.serialize()), 200
    else:
        return jsonify({
            "msg": "Not Found"
        }), 404

@app.route('/favoritos', methods = ['DELETE'])
def delete_favs():
    body = request.json
    user = get_jwt_identity()
    fav = body.get("fav_name", None)
    user_id = Usuario.query.filter_by(email = user).first()
    user_id = user_id.id
    if fav is not None:
        fav = Favorito.query.filter_by(name = fav).first()
        if fav is not None:
            try:
                db.session.delete(fav)
                db.session.commit()
                return "Eliminado", 200
            except Exception as error:
                db.session.rollback()
                return jsonify(error.args), 500
        else:
            return jsonify({
                "msg": "Favorito no existe"
            }), 404
    else:
        return jsonify({
            "msg":"Something Happened"
        }), 400

@app.route('/favoritos', methods = ['GET'])
def protected():
    user = get_jwt_identity()
    user_id = Usuario.query.filter_by(email = user).first()
    user_id = user_id.id
    favs = Favorito.query.filter_by(usuario_id = user_id)
    if favs is not None:
        favs = list(map(lambda favorito: favorito.serialize(), favs))
        return jsonify(favs)
    else:
        return jsonify({
            "msg": "No posee favoritos"
        }), 404

@app.route('/favoritos', methods = ['POST'])
def add_post ():
    user = get_jwt_identity()
    user_id = Usuario.query.filter_by(email = user).first()
    user_id = user_id.id
    body = request.json
    category = body.get("category", None)
    name = body.get("name", None)
    if category and name is not None:
        if category == "planeta":                                          
            existe_planeta = Planeta.query.filter_by(name = name).first()
            if existe_planeta is not None:
                existe_fav = Favorito.query.filter_by(name = name).first()
                if existe_fav is not None:
                    return jsonify({
                        "msg":"Planeta ya esta en favoritos"
                    })
                else:
                    try:
                        new_fav = Favorito(
                            usuario_id = user_id,
                            category = category,
                            name = name
                        )
                        db.session.add(new_fav)
                        db.session.commit()
                        return "Agregado", 200
                    except Exception as error:
                        db.session.rollback()
                        return jsonify(error), 500
            else:
                return jsonify({
                    "msg": "Planeta no existe"
                })
        if category == "personaje":                                             #AGREGAR PERSONAJE
            existe_personaje = Personaje.query.filter_by(name = name).first()
            if existe_personaje is not None:
                existe_fav = Favorito.query.filter_by(name = name).first()
                if existe_fav is not None:
                    return jsonify({
                        "msg":"Personaje ya esta en favoritos"
                    })
                else:
                    try:
                        new_fav = Favorito(
                            usuario_id = user_id,
                            category = category,
                            name = name
                        )
                        db.session.add(new_fav)
                        db.session.commit()
                        return "Agregado", 200
                    except Exception as error:
                        db.session.rollback()
                        return jsonify(error), 500
            else:
                return jsonify({
                    "msg": "Personaje no existe"
                })
    else:
        return jsonify({
            "msg": "must have a category and a name"
        }), 401



if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)