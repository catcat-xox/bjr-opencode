from app.errors import ValidationError


def _is_integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _require_object(data):
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")
    return data


def validate_item_payload(data):
    """Validate and normalize the payload for creating an item."""
    payload = _require_object(data)

    name = payload.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("name is required")

    total_stock = payload.get("total_stock")
    if not _is_integer(total_stock) or total_stock < 0:
        raise ValidationError("total_stock must be a non-negative integer")

    return {"name": name.strip(), "total_stock": total_stock}


def validate_loan_payload(data):
    """Validate and normalize the payload for creating a loan."""
    payload = _require_object(data)

    student_id = payload.get("student_id")
    if not isinstance(student_id, str) or not student_id.strip():
        raise ValidationError("student_id is required")

    item_id = payload.get("item_id")
    if not _is_integer(item_id) or item_id <= 0:
        raise ValidationError("item_id must be a positive integer")

    quantity = payload.get("quantity")
    if not _is_integer(quantity) or quantity <= 0:
        raise ValidationError("quantity must be a positive integer")

    return {
        "student_id": student_id.strip(),
        "item_id": item_id,
        "quantity": quantity,
    }


def validate_student_id(student_id):
    """Validate and normalize a student id used for loan history lookups."""
    if not isinstance(student_id, str) or not student_id.strip():
        raise ValidationError("student_id is required")
    return student_id.strip()
