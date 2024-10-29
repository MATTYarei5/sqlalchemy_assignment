from flask import jsonify, request

from models.company import Companies
from db import db


def add_company(request):
    post_data = request.form if request.form else request.json

    fields = ['company_name']
    required_fields = ['company_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field_data in required_fields and not field_data:
            return jsonify({"message": "required field missig"}), 400

        values[field] = field_data

    new_company = Companies(values['company_name'])

    db.session.add(new_company)
    db.session.commit()

    query = db.session.query(Companies).filter(Companies.company_name == values['company_name']).first()

    company = {
        "company_id": query.company_id,
        "company_name": query.company_name
    }

    return jsonify({"message": "company created", "result": company}), 201


def get_all_companies():
    companies_query = db.session.query(Companies).all()
    company_list = []

    for company in companies_query:
        company_dict = {
            "company_id": company.company_id,
            "company_name": company.company_name
        }

        company_list.append(company_dict)

    return jsonify({"message": "companies retrieved", "result": company}), 200


def get_company_by_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "company not found"}), 404

    company = {
        "company_id": company_query.company_id,
        "company_name": company_query.company_name
    }

    return jsonify({"message": "company retrieved", "result": company}), 200


def update_company(company_id, request):
    post_data = request.form if request.form else request.json

    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    company_query.company_name = post_data.get('company_name', company_query)

    company = {
        "company_id": company_query.company_id,
        "company_name": company_query.company_name
    }

    if not company_query:
        return jsonify({"message": "company not found"}), 404

    db.session.commit()

    return jsonify({"message": "company updated", "result": company}), 200


def delete_company(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "company not found"}), 404

    try:
        db.session.delete(company_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error deleting company"}), 400

    return jsonify({"message": "company deleted"}), 200
