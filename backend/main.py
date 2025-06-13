from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS
from dbms.dict_db.model import Model

app = Flask(__name__)
CORS(app)

# Blueprint with URL prefix
api = Blueprint('api', __name__)
model = Model()

@api.route('/', methods=["GET"])
def index():
    return jsonify({
        "message": "📚 Simple DBMS API is running!",
        "endpoints": {
            "POST /api/keys": "Create a key-value pair",
            "GET /api/keys/<key>": "Read a value by key",
            "PUT /api/keys/<key>": "Update a value by key",
            "DELETE /api/keys/<key>": "Delete a key",
            "GET /api/debug": "Print internal database (dev only)"
        }
    })

@api.route('/keys', methods=["POST"])
def create_name():
    data_dict = request.get_json()
    if "key" not in data_dict:
        return jsonify({"errorMsg": "bad request"}), 400
    if not model.create(data_dict["key"], data_dict):
        return jsonify({"errorMsg": "key already exists"}), 400
    return jsonify(data_dict), 201

@api.route('/keys/<key>', methods=["GET"])
def read_name(key):
    value = model.read(key)
    if value is None:
        return jsonify({"key": key, "errorMsg": "not found"}), 404
    value["key"] = key
    return jsonify(value), 200

@api.route('/keys/<key>', methods=["PUT"])
def update_name(key):
    value = request.get_json()
    if not model.update(key, value):
        return jsonify({"key": key, "errorMsg": "bad request"}), 400
    value["key"] = key
    return jsonify(value), 200

@api.route('/keys/<key>', methods=["DELETE"])
def delete_name(key):
    value = model.read(key)
    if not value or not model.delete(key):
        return jsonify({"key": key, "errorMsg": "not found"}), 404
    value["key"] = key
    return jsonify(value), 200

@api.route('/debug', methods=["GET"])
def print_database():
    database = model.debug()
    if database is None:
        return jsonify({"errorMsg": "Debug Method Not Implemented"}), 200
    return jsonify(database), 200

# Register the blueprint
app.register_blueprint(api, url_prefix='/api')

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

