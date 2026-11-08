import importlib

import database


def test_get_users_returns_only_names(tmp_path, monkeypatch):
    database_path = tmp_path / "users.db"
    monkeypatch.setattr(database, "DATABASE_PATH", str(database_path))
    database.create_db_table()
    database.insert_user({
        "name": "First User",
        "email": "first@example.com",
        "phone": "12345678",
        "address": "Beirut",
        "country": "Lebanon",
    })

    app_module = importlib.import_module("app_get_users")
    app_module = importlib.reload(app_module)
    app_module.app.config["TESTING"] = True

    response = app_module.app.test_client().get("/get_users")

    assert response.status_code == 200
    assert response.get_json() == ["First User"]
