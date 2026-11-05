def test_history_for_student_with_transactions(
    client, create_item, create_loan
):
    item = create_item(total_stock=10)
    create_loan(student_id="20240001", item_id=item["id"], quantity=1)
    create_loan(student_id="20240001", item_id=item["id"], quantity=2)

    response = client.get("/loans/student/20240001")

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert all(loan["student_id"] == "20240001" for loan in data)


def test_history_for_student_without_transactions(client):
    response = client.get("/loans/student/99999999")

    assert response.status_code == 200
    assert response.get_json() == []


def test_history_only_contains_requested_student(
    client, create_item, create_loan
):
    item = create_item(total_stock=10)
    create_loan(student_id="20240001", item_id=item["id"], quantity=1)
    create_loan(student_id="20240002", item_id=item["id"], quantity=1)

    response = client.get("/loans/student/20240001")

    data = response.get_json()
    assert len(data) == 1
    assert data[0]["student_id"] == "20240001"
