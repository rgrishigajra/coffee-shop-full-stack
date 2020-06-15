import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, NotFound, PreconditionFailed
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
import sys
app = Flask(__name__)
setup_db(app)
CORS(app)

'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES
'''
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
#get routes
@app.route('/drinks', methods=["GET"])
def get_drinks():
    print('\n\nGet /drinks hit:')
    drinks = Drink.query.all()
    if drinks is None:
        abort(404)
    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in drinks]
    })


'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=["GET"])
@requires_auth('get:drinks-detail')
def get_detailed_drinks(jwt):
    try:
        print('\n\nGet /drinks-detail hit:\n\n')
        drinks = Drink.query.all()
        if drinks is None:
            abort(404)
        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in drinks]
        })
    except Exception as e:
        print(e,sys.exc_info())
        raise(AuthError)


'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
# POST routes
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
    try:
        data = request.get_json()
        print("\n\nPOST drinks hit:", data, '\n\n')
        req_recipe = data['recipe']
        if isinstance(req_recipe, dict):
            req_recipe = [req_recipe]
        drink = Drink(title=data['title'], recipe=json.dumps(req_recipe))
        print(drink)
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': drink.long()
        })
    except:
        print(sys.exc_info())
        abort(400)


'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
#PATCH routes
@app.route('/drinks/<int:id>',methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(jwt,id):
    try:
        data = request.get_json()
        print('\n\nPatch drink hit:', id, data, '\n\n')
        drink=Drink.query.get(id)
        if drink is None:
            abort(404)
        if 'title' in data:
            drink.title=data['title']
        if 'recipe' in data:
            drink.recipe=json.dumps(data['recipe'])
        drink.update()
        print(drink)
        return jsonify({
            "success": True,
            "drinks":[drink.long()]
        })
    except NotFound:
        print(sys.exc_info())
        abort(404)
    except:
        print(sys.exc_info())
        abort(400)


'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
#DELETE Routes
@app.route('/drinks/<int:id>',methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt,id):
    print('\n\nDelete /drinks hit:',id)
    try:
        drink=Drink.query.get(id)
        print(drink)
        if drink is None:
            abort(404)
        print(drink)
        drink.delete()
        return jsonify({
            "success":True,
            "deleted":id
        })
    except NotFound:
        abort(404)
    except:
        print(sys.exc_info())
        abort(400)

# error handlers :
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


@app.errorhandler(412)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 412,
        "message": "Precondition for resouce failed",
        "question": False
    }), 412


@app.errorhandler(404)
def error_resource_not_found(error):
    return jsonify({
        "success": False,
        "message": "Resource not found",
        "error": 404
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "message": "Internal server error",
        "error": 500
    }), 500


@app.errorhandler(422)
def not_processable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Request cant be processed"
    }), 422


@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405

@app.errorhandler(401)
def auth_error(error):
    return jsonify({
        "success":False,
        "error":401,
        "message":"Not Authorized"
    })
@app.errorhandler(403)
def auth_error(error):
    return jsonify({
        "success":False,
        "error":403,
        "message":"Forbidden"
    }),403
@app.errorhandler(AuthError)
def auth_error(error):
    print(error)
    return jsonify({
        "success":False,
        "error":error.status_code,
        "message":error.error
    }),error.status_code