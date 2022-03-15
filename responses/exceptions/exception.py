# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 09:09:14 2022

@author: Admin
"""
from flask import jsonify
from singleton import Singleton

class APIError(Exception):
    """All custom API Exceptions"""
    pass


class APIAuthError(APIError):
    """Custom Authentication Error Class."""
    code = 403
    status = "Authentication Error"


from flask import Blueprint

exception_bp = Blueprint('exception_bp', __name__)

@exception_bp.app_errorhandler(APIError)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = {"code": err.code, "status": err.status, "data": None, "errors": None}
    if len(err.args) > 0:
        response["errors"] = err.args
    return jsonify(response), err.code

@exception_bp.app_errorhandler(500)
def handle_exception_500(err):
    response = {"code": 500, "status": "Internal Server Error", "data": None, "errors": ["Internal Server Error"]}
    return jsonify(response), 500
    