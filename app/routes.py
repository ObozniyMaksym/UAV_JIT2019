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
drone = 0
location = 0

@app.route('/sendHomePosition', methods = ['POST'])
def makeHome():
    global location
    location = request.get_json()
    return jsonify(location)


@app.route('/sendDroneAlgo', methods = ['POST'])
def sendDroneAlgo():
    global main
    main = DroneAlgo()
    main.get_dps(location)
    
    main.setDrone(drone);
    main.initialize();
    print(main.lx)
    main.points = request.get_json()
    main.solve() 
    print(main.lx, main.ly)
    return jsonify(main.result)

@app.route('/sendConstructive', methods = ['POST'])
def sendConstructive():
    global main
    main = Construct()
    main.get_dps(location)
    
    main.setDrone(drone);
    main.initialize();
    main.points = request.get_json()
    #main.nn = len(main.points)
    main.solve() 
    return jsonify(main.result)

@app.route('/sendInfo', methods = ['POST'])
def sendInfo():
    global drone
    drone = request.get_json()
    return jsonify(drone)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

    