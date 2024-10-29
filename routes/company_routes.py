from flask import request, Blueprint

import controllers

company = Blueprint("company", __name__)


@company.route("/company", methods=["POST"])
def add_company():
    return controllers.add_company(request)


@company.route("/companies", methods=["GET"])
def get_all_companies():
    return controllers.get_all_companies()


@company.route("/company/<company_id>", methods=["GET"])
def get_company_by_id(company_id):
    return controllers.get_company_by_id(company_id)


@company.route("/company/<company_id>", methods=["PUT"])
def update_company(company_id):
    return controllers.update_company(company_id, request)


@company.route("/company/delete/<company_id>", methods=["DELETE"])
def delete_company(company_id):
    return controllers.delete_company(company_id)
