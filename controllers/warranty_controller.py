from flask import jsonify, request

from models.warranty import Warranties

from db import db


def add_warranty():
    post_data = request.form if request.form else request.json

    fields = ['warranty_months', 'product_id']
    required_fields = ['warranty_months', 'product_id']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": "required field missing"}), 400

        values[field] = field_data

    new_warranty = Warranties(values['warranty_months'], values['product_id'])

    db.session.add(new_warranty)
    db.session.commit()

    query = db.session.query(Warranties).filter(Warranties.warranty_months == values['warranty_months']).first()

    warranty = {
        "warranty_id": query.warranty_id,
        "warranty_months": query.warranty_months
    }

    return jsonify({"message": "warranty created", "result": warranty}), 201


def get_all_warranties():
    warranties = db.session.query(Warranties).all()
    result = [
        {
            "warranty_id": warranty.warranty_id,
            "warranty_months": warranty.warranty_months
        } for warranty in warranties
    ]
    return jsonify({"message": "warranties retrieved", "result": result}), 200


def get_warranty_by_id(warranty_id):
    warranty = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty:
        return jsonify({"message": "warranty not found"}), 404

    warranty_dict = {
        "warranty_id": warranty.warranty_id,
        "warranty_months": warranty.warranty_months
    }

    return jsonify({"message": "warranty found", "result": warranty_dict}), 200


def update_warranty(warranty_id):
    post_data = request.form if request.form else request.json

    fields = ['warranty_months']
    values = {}

    for field in fields:
        field_data = post_data.get(field)
        values[field] = field_data

    warranty = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty:
        return jsonify({"message": "warranty not found"}), 404

    for key, value in values.items():
        if value:
            setattr(warranty, key, value)

    db.session.commit()

    updated_warranty = {
        "warranty_id": warranty.warranty_id,
        "warranty_months": warranty.warranty_months
    }

    return jsonify({"message": "warranty updated", "result": updated_warranty}), 200


def delete_warranty(warranty_id):
    warranty = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty:
        return jsonify({"message": "warranty not found"}), 404

    try:
        db.session.delete(warranty)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error deleting warranty"}), 400

    return jsonify({"message": "warranty deleted"}), 200
