#!/usr/bin/env python3

from flask import request
from config import app, db
from models import Owner, Pet, Shelter

# ROUTES #######################

@app.get('/owners')
def all_owners():
    owners = Owner.query.all()
    owner_dicts = [ 
        owner.to_dict(rules=("-pets",)) 
        for owner 
        in owners 
    ]
    return owner_dicts, 200

@app.get('/owners/<int:id>')
def owner_by_id(id):
    owner = Owner.query.where(Owner.id == id).first()
    if owner:
        return owner.to_dict(), 200
    else:
        return { 'error': 'Not found' }, 404
    
@app.post('/owners')
def post_owner():
    try:
        body = request.json
        new_owner = Owner(name=body.get('name'))
        db.session.add(new_owner)
        db.session.commit()
        return new_owner.to_dict(), 201
    except ValueError as e:
        return { 'error': f"Validation Error: {str(e)}" }, 400
    except Exception as e:
        return { 'error': str(e) }, 400
    
@app.post('/pets')
def post_pet():
    try:
        body = request.json
        new_pet = Pet(
            animal_type=body.get('animal_type'),
            name=body.get('name'),
            owner_id=body.get('owner_id'),
            shelter_id=body.get('shelter_id')
        )
        db.session.add(new_pet)
        db.session.commit()
        return new_pet.to_dict(), 201
    except ValueError as e:
        return { 'error': f"Validation Errors: {str(e)}" }, 400
    except Exception as e:
        return { 'error': str(e) }, 400
    
@app.patch('/shelters/<int:id>')
def patch_shelter(id):
    shelter = Shelter.query.where(Shelter.id == id).first()
    if shelter:
        try:
            body = request.json
            for key in body:
                setattr(shelter, key, body[key])
            db.session.add(shelter)
            db.session.commit()
            return shelter.to_dict(), 202
        except ValueError as e:
            return { 'error': f"Validation Errors: {str(e)}" }, 400
        except Exception as e:
            return { 'error': str(e) }, 400
    else:
        return { 'error': "Not found" }, 404
    
@app.delete('/pets/<int:id>')
def delete_pet(id):
    pet = Pet.query.where(Pet.id == id).first()
    if pet:
        db.session.delete(pet)
        db.session.commit()
        return {}, 204
    else:
        return { 'error': 'Not found' }, 404
    
@app.delete('/owner/<int:id>')
def delete_owner(id):
    owner = Owner.query.where(Owner.id == id).first()
    if owner:
        db.session.delete(owner)
        db.session.commit()
        return {}, 204
    else:
        return { 'error': 'Not found' }, 404



# RUN ##########################

if __name__ == '__main__':
    app.run(port=5555, debug=True)