from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # no serializar passworld, brecha de seguridad
        }

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    url = db.Column(db.String(120))

    def __repr__(self):
        return '<Person %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url":self.url,
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    url = db.Column(db.String(120))

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url":self.url,
        }


class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    person_id= db.Column(db.Integer, db.ForeignKey("person.id"))
    user= db.relationship(User)
    planet= db.relationship(Planet)
    person= db.relationship(Person)


    def __repr__(self):
        return '<Favourite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "person_id": self.person_id,
            
        }