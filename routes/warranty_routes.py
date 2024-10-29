from flask import request, Blueprint

import controllers

warranties = Blueprint("warranties", __name__)


@warranties.route("/warranty", methods=["POST"])
def add_warranty():
    return controllers.add_warranty()


@warranties.route("/warranties", methods=["GET"])
def get_all_warranties():
    return controllers.get_all_warranties()


@warranties.route("/warranty/<warranty_id>", methods=["GET"])
def get_warranty_by_id(warranty_id):
    return controllers.get_warranty_by_id(warranty_id)


@warranties.route("/warranty/<warranty_id>", methods=["PUT"])
def update_warranty(warranty_id):
    return controllers.update_warranty(warranty_id)


@warranties.route("/warranty/delete/<warranty_id>", methods=["DELETE"])
def delete_warranty(warranty_id):
    return controllers.delete_warranty(warranty_id)
