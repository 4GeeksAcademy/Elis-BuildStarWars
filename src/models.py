from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Planets(db.Model):
    __tablename__= 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=True, nullable=False)
    terrain = db.Column(db.String(300))
    climate = db.Column(db.String(300))
    description = db.Column(db.String(2000))
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    def __repr__(self):
        return '<Planets %r>' % self.planets
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "climate": self.climate,
            "description": self.description,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period
            # do not serialize the password, its a security breach
        }
class Characters(db.Model):
    __tablename__= 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=True, nullable=False)
    description = db.Column(db.String(1000))
    gender = db.Column(db.String(300))
    mass = db.Column(db.Integer)
    def __repr__(self):
        return '<Characters %r>' % self.characters
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "gender": self.gender,
            "mass": self.mass
            # do not serialize the password, its a security breach
        }
    
class Vehicles(db.Model):
    __tablename__= 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=True, nullable=False)
    clase = db.Column(db.String(1000))
    capacidad = db.Column(db.Integer)
    length = db.Column(db.Integer)
    def __repr__(self):
        return '<Vehicles %r>' % self.vehicles
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "clase": self.clase,
            "capacidad": self.capacidad,
            "length": self.length
            # do not serialize the password, its a security breach
        }
class Favorites(db.Model):
    __tablename__= 'favorites'
    id = db.Column(db.Integer, primary_key=True) 
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    vehicles_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"))
    
    def __repr__(self):
        return '<Favorites %r>' % self.favorites
    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            "vehicles_id": self.vehicles_id,
            
            # do not serialize the password, its a security breach
        }