def create_loan(db, student_id, item_id, quantity, status="BORROWED"):
    """Insert a new loan transaction and return its id."""
    cursor = db.execute(
        """
        INSERT INTO Loan (student_id, item_id, quantity, status)
        VALUES (?, ?, ?, ?)
        """,
        (student_id, item_id, quantity, status),
    )
    return cursor.lastrowid


def get_loan_by_id(db, loan_id):
    """Return a single loan or None when it does not exist."""
    return db.execute(
        """
        SELECT id, student_id, item_id, quantity, status, created_at
        FROM Loan
        WHERE id = ?
        """,
        (loan_id,),
    ).fetchone()


def update_loan_status(db, loan_id, status):
    """Update a loan status; return True when a row was changed."""
    cursor = db.execute(
        """
        UPDATE Loan
        SET status = ?
        WHERE id = ?
        """,
        (status, loan_id),
    )
    return cursor.rowcount == 1


def get_loans_by_student_id(db, student_id):
    """Return loans for one student, newest first."""
    return db.execute(
        """
        SELECT id, student_id, item_id, quantity, status, created_at
        FROM Loan
        WHERE student_id = ?
        ORDER BY created_at DESC, id DESC
        """,
        (student_id,),
    ).fetchall()
