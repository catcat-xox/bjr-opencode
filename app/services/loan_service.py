from app.database import get_db
from app.errors import (
    InsufficientStockError,
    InvalidLoanStateError,
    NotFoundError,
)
from app.repositories import item_repository, loan_repository
from app.validators import validate_loan_payload, validate_student_id


def create_loan(data):
    """Validate and persist a loan while decreasing stock atomically."""
    payload = validate_loan_payload(data)

    db = get_db()
    try:
        item = item_repository.get_item_by_id(db, payload["item_id"])
        if item is None:
            raise NotFoundError("Item not found")

        if item["available_stock"] < payload["quantity"]:
            raise InsufficientStockError("Insufficient stock")

        stock_decreased = item_repository.decrease_available_stock(
            db, payload["item_id"], payload["quantity"]
        )
        if not stock_decreased:
            raise InsufficientStockError("Insufficient stock")

        loan_id = loan_repository.create_loan(
            db,
            payload["student_id"],
            payload["item_id"],
            payload["quantity"],
        )
        db.commit()
    except Exception:
        db.rollback()
        raise

    return dict(loan_repository.get_loan_by_id(db, loan_id))


def return_loan(loan_id):
    """Mark a borrowed loan as returned and restore its stock atomically."""
    db = get_db()
    try:
        loan = loan_repository.get_loan_by_id(db, loan_id)
        if loan is None:
            raise NotFoundError("Loan not found")
        if loan["status"] == "RETURNED":
            raise InvalidLoanStateError("Loan has already been returned")
        if loan["status"] != "BORROWED":
            raise InvalidLoanStateError("Loan cannot be returned")

        status_updated = loan_repository.update_loan_status(
            db, loan_id, "RETURNED", expected_status="BORROWED"
        )
        if not status_updated:
            raise InvalidLoanStateError("Loan has already been returned")

        stock_restored = item_repository.increase_available_stock(
            db, loan["item_id"], loan["quantity"]
        )
        if not stock_restored:
            raise InvalidLoanStateError("Unable to restore stock")

        db.commit()
    except Exception:
        db.rollback()
        raise

    return dict(loan_repository.get_loan_by_id(db, loan_id))


def get_student_loans(student_id):
    """Return the loan history for one student."""
    normalized_student_id = validate_student_id(student_id)

    db = get_db()
    return [
        dict(row)
        for row in loan_repository.get_loans_by_student_id(
            db, normalized_student_id
        )
    ]
