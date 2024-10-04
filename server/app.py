# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)


@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.get(id)

    if not pet:
        return {'messsage': f'Pet with ID {id} not found.'}, 404

    return pet.to_dict()


@app.route('/species/<species>')
def pets_by_species(species):
    pets = Pet.query.filter_by(species=species.capitalize()).all()

    if not pets:
        return {'message': f'Not pets found with species {species}'}, 404

    return {'count': len(pets), 'pets': [pet.to_dict() for pet in pets]}


if __name__ == '__main__':
    app.run(port=5555, debug=True)
