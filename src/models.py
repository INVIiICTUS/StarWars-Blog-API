from unicodedata import category
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    favorito = db.relationship("Favorito", back_populates = "usuario", uselist = False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    nombre = db.Column(db.String(50), nullable = False)
    apellido = db.Column(db.String(50), nullable = True)



    def __repr__(self):
        return '<Usuario %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
        }

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    usuario = db.relationship("Usuario", back_populates = "favorito")
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable = False)

    category = db.Column(db.String(50))
    name = db.Column(db.String(50))


    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "category" : self.category,
            "name" : self.name

        }

class Planeta(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(30), nullable = False)
    population = db.Column(db.Integer, nullable = False)
    climate = db.Column(db.String(30), nullable = False)
    terrain = db.Column(db.String(30), nullable = False)
    gravity = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return '<Planeta %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "gravity": self.gravity
        }

class Personaje(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(30), nullable = False)
    hair_color = db.Column(db.String(30), nullable = False)
    eyes_color = db.Column(db.String(30), nullable = False)
    gender = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return '<Personaje %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.name,
            "hair_color": self.hair_color,
            "eye_color": self.eyes_color,
            "gender":self.gender
        }