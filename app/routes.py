from flask import Blueprint,jsonify

main = Blueprint('main',__name__)

@main.route("/api/v1/ping",methods = ['GET'])
def ping():
    return jsonify({'message':'pong.'})