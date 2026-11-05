def create_item(db, name, total_stock):
    """Insert a new item and initialize available_stock from total_stock."""
    cursor = db.execute(
        """
        INSERT INTO Item (name, total_stock, available_stock)
        VALUES (?, ?, ?)
        """,
        (name, total_stock, total_stock),
    )
    return cursor.lastrowid


def get_all_items(db):
    """Return every item ordered by id."""
    return db.execute(
        """
        SELECT id, name, total_stock, available_stock
        FROM Item
        ORDER BY id
        """
    ).fetchall()


def get_item_by_id(db, item_id):
    """Return a single item or None when it does not exist."""
    return db.execute(
        """
        SELECT id, name, total_stock, available_stock
        FROM Item
        WHERE id = ?
        """,
        (item_id,),
    ).fetchone()


def decrease_available_stock(db, item_id, quantity):
    """Decrease stock only when enough is available; return True on success."""
    cursor = db.execute(
        """
        UPDATE Item
        SET available_stock = available_stock - ?
        WHERE id = ? AND available_stock >= ?
        """,
        (quantity, item_id, quantity),
    )
    return cursor.rowcount == 1


def increase_available_stock(db, item_id, quantity):
    """Increase stock without exceeding total_stock; return True on success."""
    cursor = db.execute(
        """
        UPDATE Item
        SET available_stock = available_stock + ?
        WHERE id = ? AND available_stock + ? <= total_stock
        """,
        (quantity, item_id, quantity),
    )
    return cursor.rowcount == 1
