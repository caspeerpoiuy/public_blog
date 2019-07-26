from flask import jsonify

from app import db
from app.api import bp


@bp.route('/ping', methods=['GET'])
def ping():
    '''前端Vue.js用来测试与后端Flask API的连通性'''
    ret = db.session.excute("select * from users")
    print(ret)
    return jsonify('Pong!')
