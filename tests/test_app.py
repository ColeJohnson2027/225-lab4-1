from main import app, init_db
import main

def test_home_page_loads(tmp_path):

    main.DATABASE = str(tmp_path / "test.db")

    app.config["TESTING"] = True

    init_db()

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Add Contact" in response.data
