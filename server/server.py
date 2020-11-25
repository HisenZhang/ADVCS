'''
@Author: HisenZhang <zhangz29@rpi.edu>
@Date: 2020-03-27 16:26:07
@LastEditors: HisenZhang <zhangz29@rpi.edu>
@LastEditTime: 2020-03-27 21:23:04
@Description: file content
'''
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import urllib

from user import *

app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return 'Hello' #app.send_static_file('index.html')


# @app.route('/display/')
# def info():
#     return message if message else 'Please scan the QR code on ticket.'


@app.route('/auth/', methods=['POST'])
def auth():
    user=request.form.get('username', None)
    token=request.form.get('token', None)
    print(user, token)
    try:
        if user not in userlist:
            return jsonify({"error": True, "msg": "No such user"})
        if userlist[user] != token:
            return jsonify({"error": True, "msg": "Mismatched token"})
        return jsonify({"error": False, "msg": "Success"})

    except:
        return jsonify({"error": True, "msg": "Unknown"})


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8421, debug = True)
