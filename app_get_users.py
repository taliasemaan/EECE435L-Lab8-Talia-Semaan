from flask import Flask, jsonify

from database import create_db_table, get_users


app = Flask(__name__)
create_db_table()


@app.route("/get_users", methods=["GET"])
def api_get_users():
    return jsonify([user["name"] for user in get_users()]), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
