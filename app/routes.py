from app import app
import sys
from flask import jsonify, render_template, request, Response
from math import cos, sqrt, exp, tan
from random import random, randint, shuffle
import json
from app.model import DroneAlgo
from app.construct import Construct
import numpy
from numpy import ndarray
import math

battery = 0
photo = 0
main = Construct()


@app.route('/sendHomePosition', methods = ['POST'])
def makeHome():
    location = request.get_json()
    main.get_dps(location)
    return jsonify(location)

@app.route('/send', methods = ['POST'])
def send():
    main.points = request.get_json()
    main.nn = len(main.points)
    main.solve() 
    return jsonify(main.result)

@app.route('/sendInfo', methods = ['POST'])
def sendInfo():
    drone = request.get_json()
    main.setDrone(drone);
    main.initialize();
    return jsonify(main.lx)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

    