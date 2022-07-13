# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 09:09:14 2022

@author: Admin
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException
from .error_response import error_response
from flask import Blueprint

exception_bp = Blueprint('exception_bp', __name__)

@exception_bp.app_errorhandler(Exception)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = None
    if hasattr(err, 'code') and hasattr(err, 'status'):
        response = {"code": err.code, "status": err.status, "data": None, "errors": None}
    else:
        response = {"code": 500, "status": "Internal Server Error", "data": None, "errors": None}
    if len(err.args) > 0:
        response["errors"] = err.args
        arg = str(err.args[0])
        if arg.find("psycopg2.errors.UniqueViolation") != -1:
            keyStr = "Key ("
            start = arg.find(keyStr)
            if start != -1:
                end = arg.find(")=(")
                if end != -1:
                    response["errors"] = ["{} already exists".format(arg[start+len(keyStr):end])]
    return jsonify(response), 500

@exception_bp.app_errorhandler(HTTPException)
def handle_http_exception(err):
    return jsonify({"code": err.code, "status": err.name, "data": None, "errors": err.description if isinstance(err.description, list) else [err.description]}), err.code

@exception_bp.app_errorhandler(500)
@error_response
def handle_exception_500():
    return 500, "Internal Server Error", ["Internal Server Error"]
    