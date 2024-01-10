from flask import Blueprint, request, abort, Response, json
from modules.service.todo import get_todo as service_get_todo, create_todo as service_create_todo, \
    list_todos as service_list_todos, update_todo as service_update_todo, delete_todo as service_delete_todo, TodoDTO
from werkzeug.exceptions import HTTPException

todo = Blueprint("todo", __name__)


@todo.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@todo.get("/todos")
def list_todo():
    resp = service_list_todos()
    return list(map(lambda dto: dto_to_json(dto), resp))


@todo.get("/todo/<todo_id>")
def get_todo(todo_id):
    resp = service_get_todo(todo_id)
    if resp is None:
        abort(404, "Todo with this name does not exist")

    return dto_to_json(resp)


@todo.post("/todo")
def create_todo():
    data = request.get_json()
    resp = service_create_todo(TodoDTO(name=data['name'], description=data['description']))
    return dto_to_json(resp)


@todo.put("/todo")
def update_todo():
    data = request.get_json()
    resp = service_update_todo(TodoDTO(name=data['name'], description=data['description']))
    return dto_to_json(resp)


@todo.delete("/todo/<todo_id>")
def delete_todo(todo_id: str):
    resp = get_todo(todo_id)
    if resp is None:
        abort(404, "Todo with this name does not exist")
    service_delete_todo(todo_id)

    return Response(status=200)


def dto_to_json(dto: TodoDTO):
    return {
        'name': dto.name,
        'description': dto.description
    }
