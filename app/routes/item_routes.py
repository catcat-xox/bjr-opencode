from flask import Blueprint, jsonify, request

from app.services import item_service

bp = Blueprint("items", __name__, url_prefix="/items")


@bp.get("")
def list_items():
    return jsonify(item_service.list_items()), 200


@bp.post("")
def create_item():
    data = request.get_json(silent=True)
    item = item_service.create_item(data)
    return jsonify(item), 201
