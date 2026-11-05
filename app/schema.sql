-- Skema database Lab Equipment Loan System.
-- Dijalankan secara idempotent saat aplikasi dibuat.

CREATE TABLE IF NOT EXISTS Item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    total_stock INTEGER NOT NULL CHECK (total_stock >= 0),
    available_stock INTEGER NOT NULL
        CHECK (available_stock >= 0 AND available_stock <= total_stock)
);

CREATE TABLE IF NOT EXISTS Loan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL CHECK (length(trim(student_id)) > 0),
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    status TEXT NOT NULL DEFAULT 'BORROWED'
        CHECK (status IN ('BORROWED', 'RETURNED', 'CANCELLED')),
    created_at TIMESTAMP NOT NULL
        DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    FOREIGN KEY (item_id) REFERENCES Item (id)
);

CREATE INDEX IF NOT EXISTS idx_loan_student_id ON Loan (student_id);
CREATE INDEX IF NOT EXISTS idx_loan_item_id ON Loan (item_id);
