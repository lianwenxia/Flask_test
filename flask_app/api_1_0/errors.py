from flask import request, jsonify
import json

def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    print(403)
    print(response.json)
    return response


def not_exit(message):
    response = jsonify({'error': 'does not exit', 'message': message})
    response.status_code = 401
    # print(401)
    # print(response.json)
    return response