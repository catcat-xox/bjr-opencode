def test_index_page_renders_dashboard(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.mimetype == "text/html"

    html = response.get_data(as_text=True)
    assert "Lab Equipment Loan System" in html
    assert 'id="item-form"' in html
    assert 'id="loan-form"' in html
    assert 'id="history-form"' in html
    assert 'id="items-body"' in html
    assert "/static/js/app.js" in html


def test_index_links_stylesheet(client):
    html = client.get("/").get_data(as_text=True)

    assert "/static/css/style.css" in html


def test_static_stylesheet_is_served(client):
    response = client.get("/static/css/style.css")

    assert response.status_code == 200
    assert response.mimetype == "text/css"
    assert "--primary" in response.get_data(as_text=True)


def test_static_javascript_is_served(client):
    response = client.get("/static/js/app.js")

    assert response.status_code == 200
    assert "javascript" in response.mimetype
    assert "loadItems" in response.get_data(as_text=True)
    assert "/loans/student/" in response.get_data(as_text=True)


def test_web_page_and_api_share_same_app(app):
    with app.test_client() as client:
        assert client.get("/").status_code == 200
        assert client.get("/items").status_code == 200
