import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    return create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "lab_equipment_test.db"),
        }
    )


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def create_item(client):
    def _create_item(name="Multimeter", total_stock=10):
        response = client.post(
            "/items",
            json={"name": name, "total_stock": total_stock},
        )
        assert response.status_code == 201
        return response.get_json()

    return _create_item


@pytest.fixture
def create_loan(client):
    def _create_loan(student_id="20240001", item_id=1, quantity=1):
        response = client.post(
            "/loans",
            json={
                "student_id": student_id,
                "item_id": item_id,
                "quantity": quantity,
            },
        )
        assert response.status_code == 201
        return response.get_json()

    return _create_loan
