import importlib

import pytest

import database


@pytest.fixture
def database_path(tmp_path, monkeypatch):
    path = tmp_path / "users.db"
    monkeypatch.setattr(database, "DATABASE_PATH", str(path))
    return path


@pytest.fixture
def initialized_database(database_path):
    database.create_db_table()
    return database_path


@pytest.fixture
def app_client(database_path):
    app_module = importlib.import_module("app")
    app_module = importlib.reload(app_module)
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


def sample_user(**overrides):
    user = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "12345678",
        "address": "Beirut",
        "country": "Lebanon",
    }
    user.update(overrides)
    return user


def test_database_is_created_when_app_first_runs(app_client, database_path):
    assert database_path.exists()
    assert database.get_users() == []


def test_insert_user(initialized_database):
    user = database.insert_user(sample_user())

    assert user["user_id"] > 0
    assert user["name"] == "Test User"
    assert user["email"] == "test@example.com"


def test_get_users(initialized_database):
    first_user = database.insert_user(sample_user())
    second_user = database.insert_user(
        sample_user(name="Second User", email="second@example.com")
    )

    assert database.get_users() == [first_user, second_user]


def test_get_user_by_id(initialized_database):
    inserted_user = database.insert_user(sample_user())

    assert database.get_user_by_id(inserted_user["user_id"]) == inserted_user
    assert database.get_user_by_id(-1) is None


def test_update_user(initialized_database):
    inserted_user = database.insert_user(sample_user())
    updated_data = sample_user(
        name="Updated User",
        email="updated@example.com",
        user_id=inserted_user["user_id"],
    )

    updated_user = database.update_user(updated_data)

    assert updated_user == updated_data
    assert database.update_user(sample_user(user_id=-1)) is None


def test_delete_user(initialized_database):
    inserted_user = database.insert_user(sample_user())

    assert database.delete_user(inserted_user["user_id"]) is True
    assert database.get_user_by_id(inserted_user["user_id"]) is None
    assert database.delete_user(inserted_user["user_id"]) is False


def test_api_get_user(app_client):
    inserted_user = database.insert_user(sample_user())

    response = app_client.get(f"/api/users/{inserted_user['user_id']}")

    assert response.status_code == 200
    assert response.get_json() == inserted_user


def test_api_add_user(app_client):
    user = sample_user()

    response = app_client.post("/api/users/add", json=user)

    assert response.status_code == 201
    assert response.get_json()["user_id"] > 0
    assert {key: response.get_json()[key] for key in user} == user


def test_api_update_user(app_client):
    inserted_user = database.insert_user(sample_user())
    updated_user = sample_user(
        name="Updated User",
        email="updated@example.com",
        user_id=inserted_user["user_id"],
    )

    response = app_client.put("/api/users/update", json=updated_user)

    assert response.status_code == 200
    assert response.get_json() == updated_user


def test_api_delete_user(app_client):
    inserted_user = database.insert_user(sample_user())

    response = app_client.delete(
        f"/api/users/delete/{inserted_user['user_id']}"
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "User deleted successfully",
        "user_id": inserted_user["user_id"],
    }
    assert database.get_user_by_id(inserted_user["user_id"]) is None
