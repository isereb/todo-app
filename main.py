from flask import Flask, jsonify
from api.v1.todo import todo
from datetime import datetime
import awsgi

app = Flask(__name__)
app.register_blueprint(todo, url_prefix="/api/v1")
app.json.sort_keys = False


@app.get("/")
def home():
    return jsonify({
        "name": "todo-app",
        "time_now": datetime.now().isoformat(),
    })


print(app.url_map)


# app.run(host="127.0.0.1", port=8000, debug=True)

def handler(event, context):
    return awsgi.response(app, event, context)
