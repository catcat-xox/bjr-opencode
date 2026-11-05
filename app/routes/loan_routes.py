from flask import Blueprint, jsonify, request

from app.services import loan_service

bp = Blueprint("loans", __name__, url_prefix="/loans")


@bp.post("")
def create_loan():
    data = request.get_json(silent=True)
    loan = loan_service.create_loan(data)
    return jsonify(loan), 201


@bp.put("/<int:loan_id>/return")
def return_loan(loan_id):
    loan = loan_service.return_loan(loan_id)
    return jsonify(loan), 200


@bp.get("/student/<student_id>")
def get_student_loans(student_id):
    loans = loan_service.get_student_loans(student_id)
    return jsonify(loans), 200
