import os

from modules.ddbutil.dynamo import dynamodb
from flask import abort


class TodoDTO:
    name: str
    description: str

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


table_name = os.environ.get('AWS_STACK_NAME', '') + '-table'
table = dynamodb.Table(table_name)


def list_todos():
    resp = table.scan()
    return list(map(lambda i: TodoDTO(name=i['PK'], description=i['description']), resp['Items']))


def get_todo(todo_id):
    resp = table.get_item(Key={
        'PK': todo_id
    })
    if resp['ResponseMetadata']['HTTPStatusCode'] != 200:
        abort(500, 'Something went wrong')
    i = resp.get('Item')
    if i is None:
        return None

    dto = TodoDTO(name=i['PK'], description=i['description'])

    return dto


def create_todo(todo: TodoDTO):
    was_found = False

    item = get_todo(todo.name)
    if item is not None:
        abort(400, 'Todo with this name already exists')

    resp = table.put_item(Item={
        'PK': todo.name,
        'description': todo.description
    })

    return todo


def update_todo(todo: TodoDTO):
    item = get_todo(todo.name)
    if item is None:
        abort(400, 'Todo with this name does not exist')

    resp = table.update_item(
        Key={'PK': todo.name},
        UpdateExpression="set description = :description",
        ExpressionAttributeValues={
            ':description': todo.description
        },
        ReturnValues='UPDATED_NEW')

    return get_todo(todo.name)


def delete_todo(todo_id):
    resp = table.delete_item(Key={
        'PK': todo_id
    })
    if resp['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise abort(500, 'Something went wrong')
