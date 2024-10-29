from flask import jsonify, request

from models.category import Categories
from db import db


def add_category():
    post_data = request.form if request.form else request.json

    fields = ['category_name']
    required_fields = ['category_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": "required field missing"}), 400

        values[field] = field_data

    new_category = Categories(category_name=values['category_name'])

    db.session.add(new_category)
    db.session.commit()

    query = db.session.query(Categories).filter(Categories.category_name == values['category_name']).first()

    category = {
        "category_id": query.category_id,
        "category_name": query.category_name
    }

    return jsonify({"message": "category created", "result": category}), 201


def get_all_categories():
    categories = db.session.query(Categories).all()
    result = [
        {
            "category_id": category.category_id,
            "category_name": category.category_name
        } for category in categories
    ]
    return jsonify({"message": "categories retrieved", "result": result}), 200


def get_category_by_id(category_id):
    category = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category:
        return jsonify({"message": "category not found"}), 404

    category_dict = {
        "category_id": category.category_id,
        "category_name": category.category_name
    }

    return jsonify({"message": "category found", "result": category_dict}), 200


def update_category(category_id):
    post_data = request.form if request.form else request.json

    fields = ['category_name']
    values = {}

    for field in fields:
        field_data = post_data.get(field)
        values[field] = field_data

    category = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category:
        return jsonify({"message": "category not found"}), 404

    for key, value in values.items():
        if value:
            setattr(category, key, value)

    db.session.commit()

    updated_category = {
        "category_id": category.category_id,
        "category_name": category.category_name
    }

    return jsonify({"message": "category updated", "result": updated_category}), 200


def delete_category(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": "category not found"}), 404

    try:
        db.session.delete(category_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error deleting category"}), 400

    return jsonify({"message": "category deleted"}), 200
