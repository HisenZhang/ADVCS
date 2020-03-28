'''
@Author: HisenZhang <zhangz29@rpi.edu>
@Date: 2020-03-27 16:26:07
@LastEditors: HisenZhang <zhangz29@rpi.edu>
@LastEditTime: 2020-03-27 16:56:17
@Description: file content
'''
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import urllib

from user import *

app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return app.send_static_file('index.html')


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


# @app.route('/qr/',methods=['POST'])
# def verify():
# 	global message
# 	data = request.form.get('data',None)
# 	# data = request.args.get('data')
# 	# print(data)
# 	data = urllib.parse.unquote(data)
# 	data = data.split('>=<')
# 	print(eval(data[1]))
# 	for i in d:
# 		if i["id"] == int(data[0]):
# 			privkey = rsa.PrivateKey.load_pkcs1(i["pvk"])
# 			try:
# 				info = rsa.decrypt(eval(data[1]), privkey).decode('utf-8')
# 				if info == i["info"]:
# 					message = "\n\nOK - ID:"+str(i["id"])+" Info:"+info+"\n\n"
# 					print(message)
# 					# return "\n\nOK - ID:"+str(i["id"])+" Info:"+info+"\n\n"
# 				else:
# 					print("Info Mismatch")
# 					# return 'Info Mismatch'
# 			except rsa.pkcs1.DecryptionError:
# 				message = "Expired"
# 				print(message)
# 				# return 'Expired'
# 	return 'Verified'

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8421, debug = True)
