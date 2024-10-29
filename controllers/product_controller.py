from flask import jsonify, request

from models.product import Products
from db import db


def add_product(request):
    post_data = request.form if request.form else request.json

    fields = ['product_name', 'description', 'price', 'company_id', 'active']
    required_fields = ['product_name', 'company_id']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field_data in required_fields and not field_data:
            return jsonify({'message': 'required field missing'}), 400

        values[field] = field_data

    new_product = Products(values['product_name'], values['description'], values['price'], values['company_id'], values['active'])

    db.session.add(new_product)
    db.session.commit()

    company_dict = {
        'company_id': new_product.company.company_id,
        'company_name': new_product.company.company_name
    }

    product_dict = {
        'product_id': new_product.product_id,
        'product_name': new_product.product_name,
        'description': new_product.description,
        'price': new_product.price,
        'active': new_product.active,
        'company': company_dict
    }

    return jsonify({'message': 'product created', 'results': product_dict}), 201


def get_all_products():
    products_query = db.session.query(Products).all()

    products_list = []

    for product in products_query:
        category_list = []

        for category in product.categories:
            category_list.append({
                'category_id': category.category_id,
                'category_name': category.category_name
            })

        company_dict = {
            'company_id': product.company.company_id,
            'company_name': product.company.company_name
        }

        if product.warranty:
            warranty_dict = {
                'warranty_id': product.warranty.warranty_id,
                'warranty_months': product.warranty.warranty_months
            }
        else:
            warranty_dict = {}

        product_dict = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'description': product.description,
            'price': product.price,
            'active': product.active,
            'company': company_dict,
            'warranty': warranty_dict,
            'categories': category_list
        }

        products_list.append(product_dict)

    return jsonify({'message': 'products found', 'results': products_list}), 200


def get_product_by_id(product_id):
    product = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product:
        return jsonify({"message": "product not found"}), 404

    category_list = [
        {
            'category_id': category.category_id,
            'category_name': category.category_name
        } for category in product.categories
    ]

    company_dict = {
        'company_id': product.company.company_id,
        'company_name': product.company.company_name
    }

    if product.warranty:
        warranty_dict = {
            'warranty_id': product.warranty.warranty_id,
            'warranty_months': product.warranty.warranty_months
        }
    else:
        warranty_dict = {}

    product_dict = {
        'product_id': product.product_id,
        'product_name': product.product_name,
        'description': product.description,
        'price': product.price,
        'active': product.active,
        'company': company_dict,
        'warranty': warranty_dict,
        'categories': category_list
    }

    return jsonify({'message': 'product found', 'results': product_dict}), 200


def update_product(product_id):
    post_data = request.form if request.form else request.json

    product = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product:
        return jsonify({"message": "product not found"}), 404

    fields = ['product_name', 'description', 'price', 'active', 'company_id', 'warranty_id']
    for field in fields:
        if field in post_data:
            setattr(product, field, post_data[field])

    db.session.commit()

    category_list = [
        {
            'category_id': category.category_id,
            'category_name': category.category_name
        } for category in product.categories
    ]

    company_dict = {
        'company_id': product.company.company_id,
        'company_name': product.company.company_name
    }

    if product.warranty:
        warranty_dict = {
            'warranty_id': product.warranty.warranty_id,
            'warranty_months': product.warranty.warranty_months
        }
    else:
        warranty_dict = {}

    updated_product_dict = {
        'product_id': product.product_id,
        'product_name': product.product_name,
        'description': product.description,
        'price': product.price,
        'active': product.active,
        'company': company_dict,
        'warranty': warranty_dict,
        'categories': category_list
    }

    return jsonify({'message': 'product updated', 'results': updated_product_dict}), 200


def delete_product(product_id):
    product = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product:
        return jsonify({"message": "product not found"}), 404

    try:
        db.session.delete(product)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error deleting product"}), 500

    return jsonify({"message": "product deleted"}), 200
