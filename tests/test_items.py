def test_get_items_when_database_is_empty(client):
    response = client.get("/items")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_item_with_valid_data(client):
    response = client.post(
        "/items",
        json={"name": "  Multimeter  ", "total_stock": 10},
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Multimeter"
    assert data["total_stock"] == 10
    assert data["available_stock"] == 10


def test_create_item_without_name(client):
    response = client.post("/items", json={"total_stock": 10})

    assert response.status_code == 400
    assert response.get_json()["error"] == "name is required"


def test_create_item_with_blank_name(client):
    response = client.post("/items", json={"name": "   ", "total_stock": 10})

    assert response.status_code == 400
    assert response.get_json()["error"] == "name is required"


def test_create_item_with_negative_stock(client):
    response = client.post(
        "/items",
        json={"name": "Multimeter", "total_stock": -1},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "total_stock must be a non-negative integer"
    )


def test_create_item_with_non_integer_stock(client):
    response = client.post(
        "/items",
        json={"name": "Multimeter", "total_stock": "10"},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "total_stock must be a non-negative integer"
    )


def test_initial_available_stock_equals_total_stock(client):
    response = client.post(
        "/items",
        json={"name": "Oscilloscope", "total_stock": 7},
    )

    data = response.get_json()
    assert data["total_stock"] == 7
    assert data["available_stock"] == 7


def test_get_items_reflects_current_stock(client, create_item):
    item = create_item(total_stock=10)
    client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 4},
    )

    response = client.get("/items")

    assert response.status_code == 200
    assert response.get_json()[0]["available_stock"] == 6


def test_create_item_rejects_non_json_body(client):
    response = client.post(
        "/items",
        data="not json",
        content_type="text/plain",
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Request body must be a JSON object"
    )


def test_unknown_route_returns_json_error(client):
    response = client.get("/unknown")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Not found"}


def test_wrong_method_returns_json_error(client):
    response = client.delete("/items")

    assert response.status_code == 405
    assert response.get_json() == {"error": "Method not allowed"}
