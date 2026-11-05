def test_return_loan_with_valid_transaction(client, create_item, create_loan):
    item = create_item(total_stock=10)
    loan = create_loan(student_id="20240001", item_id=item["id"], quantity=3)

    response = client.put(f"/loans/{loan['id']}/return")

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == loan["id"]
    assert data["status"] == "RETURNED"


def test_return_loan_restores_stock(client, create_item, create_loan):
    item = create_item(total_stock=10)
    loan = create_loan(student_id="20240001", item_id=item["id"], quantity=3)

    client.put(f"/loans/{loan['id']}/return")

    items = client.get("/items").get_json()
    assert items[0]["available_stock"] == 10


def test_return_unknown_loan(client):
    response = client.put("/loans/999/return")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Loan not found"


def test_return_loan_that_is_already_returned(
    client, create_item, create_loan
):
    item = create_item()
    loan = create_loan(student_id="20240001", item_id=item["id"], quantity=2)
    client.put(f"/loans/{loan['id']}/return")

    response = client.put(f"/loans/{loan['id']}/return")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Loan has already been returned"


def test_double_return_does_not_restore_stock_twice(
    client, create_item, create_loan
):
    item = create_item(total_stock=10)
    loan = create_loan(student_id="20240001", item_id=item["id"], quantity=4)

    first = client.put(f"/loans/{loan['id']}/return")
    second = client.put(f"/loans/{loan['id']}/return")

    assert first.status_code == 200
    assert second.status_code == 400
    assert client.get("/items").get_json()[0]["available_stock"] == 10
