from config import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates


# MODELS ################

# Owner --< Pet >-- Shelter

class Owner(db.Model, SerializerMixin):

    __tablename__ = 'owners_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # RELATIONSHIPS

    pets = db.relationship('Pet', back_populates='owner')
    shelters = association_proxy('pets', 'shelter')

    # VALIDATIONS

    @validates('name')
    def validate_name(self, key, new_value):
        if not len(new_value) >= 1:
            raise ValueError('Owner name must be at least 1 character')
        return new_value
    
class Shelter(db.Model, SerializerMixin):
    
    __tablename__ = 'shelters_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)

    # RELATIONSHIPS

    pets = db.relationship('Pet', back_populates='shelter')
    owners = association_proxy('pets', 'owner')

    # VALIDATIONS

    @validates('name', 'location')
    def validate_name(self, key, new_value):
        if not len(new_value) >= 1:
            raise ValueError(f'Shelter {key} must be at least 1 character')
        return new_value
    
class Pet(db.Model, SerializerMixin):

    __tablename__ = 'pets_table'

    id = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String)
    name = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners_table.id'))
    shelter_id = db.Column(db.Integer, db.ForeignKey('shelters_table.id'))

    # RELATIONSHIPS

    owner = db.relationship('Owner', back_populates='pets')
    shelter = db.relationship('Shelter', back_populates='pets')

    # VALIDATIONS

    @validates('name', 'animal_type')
    def validate_name(self, key, new_value):
        if not len(new_value) >= 1:
            raise ValueError(f'Pet {key} must be at least 1 character')
        return new_value