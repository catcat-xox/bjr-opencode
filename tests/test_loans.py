import pytest


def test_create_loan_with_valid_data(client, create_item):
    item = create_item(total_stock=10)

    response = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 3},
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["student_id"] == "20240001"
    assert data["item_id"] == item["id"]
    assert data["quantity"] == 3
    assert data["status"] == "BORROWED"
    assert data["created_at"]


def test_create_loan_decreases_stock(client, create_item):
    item = create_item(total_stock=10)

    client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 4},
    )

    items = client.get("/items").get_json()
    assert items[0]["available_stock"] == 6


def test_create_loan_when_quantity_exceeds_stock(client, create_item):
    item = create_item(total_stock=2)

    response = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 3},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Insufficient stock"


def test_create_loan_with_unknown_item(client):
    response = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": 999, "quantity": 1},
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "Item not found"


@pytest.mark.parametrize("quantity", [0, -1])
def test_create_loan_with_non_positive_quantity(client, create_item, quantity):
    item = create_item()

    response = client.post(
        "/loans",
        json={
            "student_id": "20240001",
            "item_id": item["id"],
            "quantity": quantity,
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "quantity must be a positive integer"
    )


def test_create_loan_without_student_id(client, create_item):
    item = create_item()

    response = client.post(
        "/loans",
        json={"item_id": item["id"], "quantity": 1},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "student_id is required"


def test_failed_loan_does_not_change_stock(client, create_item):
    item = create_item(total_stock=5)

    response = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 6},
    )

    assert response.status_code == 400
    assert client.get("/items").get_json()[0]["available_stock"] == 5
