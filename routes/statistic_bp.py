# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 00:32:26 2022

@author: Admin
"""

from flask import Blueprint
from controllers.StatisticController import *
from utils.constant import BASE_URL

statistic_bp = Blueprint('statistic_bp', __name__, url_prefix=BASE_URL+"/cameras")
statistic_bp.route('/<cameraId>/statistics', methods=['POST'])(createStatistic)
statistic_bp.route('/<cameraId>/statistics', methods=['GET'])(getStatisticByTimestamp)