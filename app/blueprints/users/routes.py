from app.blueprints.users import users_bp
from .schemas import user_schema, users_schema
from flask import request, jsonify
from marshmallow import  ValidationError
from app.models import Users, db

#================= CRUD USERS ==============================


@users_bp.route('', methods=['POST'])
def make_user():
    try:
        data = user_schema.load(request.json) # type: ignore
        print(data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_user = Users(**data)
    db.session.add(new_user)
    db.session.commit()
    print("Created new user")
    return user_schema.jsonify(new_user), 200


#endpoint to get user data
@users_bp.route('', methods=['GET'])
def read_users():
    users=db.session.query(Users).all()
    print(users)
    return users_schema.jsonify(users), 200

#endpoint to get user data
@users_bp.route('<int:user_id>', methods=['GET'])
def user_by_id(user_id):
    user=db.session.get(Users, user_id)
    print(user)
    return user_schema.jsonify(user)

#delete a user
@users_bp.route('<int:user_id>', methods=['DELETE'])
def delete_by_id(user_id):
    user=db.session.get(Users, user_id)
    db.session.delete(user)
    db.session.commit()
    print(f"deleted user at index {user_id}")
    return jsonify(f"A deleted user at index {user_id}")

#update a user NOT BUILT
@users_bp.route('<int:user_id>', methods=['PUT'])
def update_by_id(user_id):
    user=db.session.get(Users, user_id)
    print(user)
    if not user:
        return jsonify({"message": "user not found"}), 404
    else:
        try:
            user_data = user_schema.load(request.json) # type: ignore
            print(user_data)
        except ValidationError as e:
            return jsonify({"message":e.messages}), 400
        
    # user = user_data
    # db.session.commit()
    for key, value in user_data.items():
        if value: #blank fields will not be updated
            setattr(user,key,value)
    db.session.commit()

    return jsonify({"message":user_data})