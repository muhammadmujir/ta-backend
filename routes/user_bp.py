# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 20:59:57 2022

@author: Admin
"""

from flask import Blueprint
from controllers.UserController import *
from utils.constant import BASE_URL

user_bp = Blueprint('user_bp', __name__, url_prefix=BASE_URL+"/users")

# auth
user_bp.route('/_register', methods=['POST'])(register)
user_bp.route('/_login', methods=['POST'])(login)
user_bp.route('/_currentUser', methods=['GET'])(show)
user_bp.route('/_currentUser', methods=['PUT'])(updateUser)

# example
# user_bp.route('/<user_id>/<name>', methods=['GET'])(userDetail)
# user_bp.route('/', methods=['GET'])(index)
# user_bp.route('/create', methods=['GET'])(store)
# user_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
# user_bp.route('/<int:user_id>', methods=['DELETE'])(delete)
