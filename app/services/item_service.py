from app.database import get_db
from app.repositories import item_repository
from app.validators import validate_item_payload


def list_items():
    """Return every item with its current stock."""
    db = get_db()
    return [dict(row) for row in item_repository.get_all_items(db)]


def create_item(data):
    """Validate and persist a new item."""
    payload = validate_item_payload(data)

    db = get_db()
    try:
        item_id = item_repository.create_item(
            db, payload["name"], payload["total_stock"]
        )
        db.commit()
    except Exception:
        db.rollback()
        raise

    return dict(item_repository.get_item_by_id(db, item_id))
