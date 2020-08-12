import models
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

dog = Blueprint('dogs', 'dog')

@dog.route('/', methods=["GET"])
@login_required
def get_all_dogs():
    try:
        dogs = [model_to_dict(dog) for dog in models.Dog.select()]
        print(dogs)
        return jsonify(data=dogs, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@dog.route('/', methods=["POST"])
@login_required
def create_dogs():
    payload = request.get_json()
    print(type(payload), 'payload')
    new_dog = models.Dog.create(name=payload['name'], owner=current_user.id, breed=payload['breed'])
    print(model_to_dict(new_dog), 'model to dict')
    dog_data = model_to_dict(new_dog)
    return jsonify(data=dog_data, status={"code": 201, "message": "Success"})

@dog.route('/<id>', methods=["GET"])
@login_required
def get_one_dog(id):
    print(id, 'reserved word?')
    dog = models.Dog.get_by_id(id)
    print(dog.__dict__)
    return jsonify(data=model_to_dict(dog), status={"code": 200, "message": "Success"})

@dog.route('/<id>', methods=["PUT"])
@login_required
def update_dog(id):
    payload = request.get_json()
    query = models.Dog.update(**payload).where(models.Dog.id==id)
    query.execute()
    return jsonify(data=model_to_dict(models.Dog.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})

@dog.route('/<id>', methods=["Delete"])
@login_required
def delete_dog(id):
    query = models.Dog.delete().where(models.Dog.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})