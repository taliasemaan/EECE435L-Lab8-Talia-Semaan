from flask import Flask, request, jsonify
from flask_cors import CORS

from database import (
    create_db_table,
    get_users,
    get_user_by_id,
    insert_user,
    update_user,
    patch_user,
    delete_user
)


app = Flask(__name__)
CORS(app)

create_db_table()

REQUIRED_FIELDS = ["name", "email", "phone", "address", "country"]


@app.route("/")
def home():
    return jsonify({
        "message": "Flask User Management API is running"
    })


@app.route("/api/users", methods=["GET"])
def api_get_users():
    return jsonify(get_users()), 200


@app.route("/api/users/<int:user_id>", methods=["GET"])
def api_get_user(user_id):
    user = get_user_by_id(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200


@app.route("/api/users/add", methods=["POST"])
def api_add_user():
    user = request.get_json(silent=True)

    if user is None:
        return jsonify({"error": "A JSON body is required"}), 400

    missing_fields = [
        field for field in REQUIRED_FIELDS
        if field not in user or not str(user[field]).strip()
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    new_user = insert_user(user)
    return jsonify(new_user), 201


@app.route("/api/users/update", methods=["PUT"])
def api_update_user():
    user = request.get_json(silent=True)

    if user is None:
        return jsonify({"error": "A JSON body is required"}), 400

    required_put_fields = ["user_id"] + REQUIRED_FIELDS

    missing_fields = [
        field for field in required_put_fields
        if field not in user or not str(user[field]).strip()
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    updated_user = update_user(user)

    if updated_user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(updated_user), 200


@app.route("/api/users/<int:user_id>", methods=["PATCH"])
def api_patch_user(user_id):
    changes = request.get_json(silent=True)

    if changes is None or len(changes) == 0:
        return jsonify({"error": "A JSON body is required"}), 400

    allowed_fields = set(REQUIRED_FIELDS)
    invalid_fields = set(changes.keys()) - allowed_fields

    if invalid_fields:
        return jsonify({
            "error": "Invalid fields",
            "fields": sorted(invalid_fields)
        }), 400

    updated_user = patch_user(user_id, changes)

    if updated_user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(updated_user), 200


@app.route("/api/users/delete/<int:user_id>", methods=["DELETE"])
def api_delete_user(user_id):
    deleted = delete_user(user_id)

    if not deleted:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "status": "User deleted successfully",
        "user_id": user_id
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)