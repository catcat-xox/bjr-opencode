def test_full_lifecycle_keeps_stock_consistent(
    client, create_item, create_loan
):
    item = create_item(total_stock=10)

    first = create_loan(student_id="20240001", item_id=item["id"], quantity=3)
    second = create_loan(student_id="20240001", item_id=item["id"], quantity=2)
    assert client.get("/items").get_json()[0]["available_stock"] == 5

    assert client.put(f"/loans/{first['id']}/return").status_code == 200
    assert client.get("/items").get_json()[0]["available_stock"] == 8

    assert client.put(f"/loans/{second['id']}/return").status_code == 200
    assert client.get("/items").get_json()[0]["available_stock"] == 10

    history = client.get("/loans/student/20240001").get_json()
    assert len(history) == 2
    assert {loan["status"] for loan in history} == {"RETURNED"}


def test_stock_never_becomes_negative(client, create_item):
    item = create_item(total_stock=3)

    rejected = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 4},
    )
    accepted = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 3},
    )
    another_attempt = client.post(
        "/loans",
        json={"student_id": "20240002", "item_id": item["id"], "quantity": 1},
    )

    assert rejected.status_code == 400
    assert accepted.status_code == 201
    assert another_attempt.status_code == 400
    assert client.get("/items").get_json()[0]["available_stock"] == 0


def test_loan_rolls_back_when_transaction_insert_fails(
    client, app, create_item, monkeypatch
):
    item = create_item(total_stock=10)

    from app.services import loan_service

    def fail(*args, **kwargs):
        raise RuntimeError("simulated database failure")

    monkeypatch.setattr(loan_service.loan_repository, "create_loan", fail)
    app.config["PROPAGATE_EXCEPTIONS"] = False

    response = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item["id"], "quantity": 4},
    )

    assert response.status_code == 500
    assert response.get_json() == {"error": "Internal server error"}
    assert client.get("/items").get_json()[0]["available_stock"] == 10
    assert client.get("/loans/student/20240001").get_json() == []


def test_return_rolls_back_when_stock_restore_fails(
    client, create_item, create_loan, monkeypatch
):
    item = create_item(total_stock=10)
    loan = create_loan(student_id="20240001", item_id=item["id"], quantity=4)
    assert client.get("/items").get_json()[0]["available_stock"] == 6

    from app.services import loan_service

    monkeypatch.setattr(
        loan_service.item_repository,
        "increase_available_stock",
        lambda *args, **kwargs: False,
    )

    response = client.put(f"/loans/{loan['id']}/return")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Unable to restore stock"
    assert client.get("/items").get_json()[0]["available_stock"] == 6
    history = client.get("/loans/student/20240001").get_json()
    assert history[0]["status"] == "BORROWED"
