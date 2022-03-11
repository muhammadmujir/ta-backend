# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 20:59:57 2022

@author: Admin
"""

from flask import Blueprint
from controllers.UserController import index, store, show, update, delete

user_bp = Blueprint('user_bp', __name__)
user_bp.route('/', methods=['GET'])(index)
user_bp.route('/create', methods=['GET'])(store)
user_bp.route('/<int:user_id>', methods=['GET'])(show)
user_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
user_bp.route('/<int:user_id>', methods=['DELETE'])(delete)