from app import app
import sys
from flask import jsonify, render_template, request, Response
from math import cos, sqrt, exp, tan
from random import random, randint, shuffle
import json
from app.model import DroneAlgo

main = DroneAlgo()

'''
base = {"lat": 0, "lng": 0}
zero = {"x": 0, "y": 0}
dpx = 1
dpy = 1
lx = 100
ly = 100
points = []
a = []
cur_ans = 0
ans_points = []
all_points = []

#GEOMETRY 

#Distance between 2 points
def get_dist(a, b):
    return sqrt((a["x"] - b["x"]) * (a["x"] - b["x"]) + (a["y"] - b["y"]) * (a["y"] - b["y"]))

#Oriented square of triangle
def get_square(a, b, c):
    return (a["x"] - b["x"]) * (a["y"] + b["y"]) + (b["x"] - c["x"]) * (b["y"] + c["y"]) + (c["x"] - a["x"]) * (c["y"] + a["y"])

#Get dpx and dpy
def get_dps(location):
    global base
    base = location
    phi = base["lat"] / 180 * 3.1415926
    global dpx, dpy
    dpx = 111.321*cos(phi) - 0.0094*cos(3*phi)
    dpy = 111.143

#Transformation from lat/lng to cartesian coordinates
def get_distance():
    global a
    a.clear()
    for i in range(0, len(points)):
        a.append({"x": (points[i]["lng"] - base["lng"])*dpx*1000, "y": (points[i]["lat"] - base["lat"])*dpy*1000, "id": i})

#Check do the segments intersect
def intersection(a, b, c, d):
    if get_square(a, c, b) * get_square(a, d, b) < 0 and get_square(c, a, d) * get_square(c, b, d) < 0:
        return 1
    return 0

#Check is the point inside the border
def is_in(x, y):
    p = {"x": x, "y": y}
    q = {"x": 1000000000, "y": 970005041}
    kol = 0
    for i in range(0, len(a) - 1):
        if intersection(p, q, a[i], a[i + 1]) == 1:
            kol = kol + 1
    if intersection(p, q, a[0], a[-1]) == 1:
        kol = kol + 1
    if kol % 2 == 1:
        return 1
    return 0

#Check do the segment and the border intersect
def inter(x1, y1, x2, y2):
    p = {"x": x1, "y": y1}
    q = {"x": x2, "y": y2}
    for i in range(0, len(a) - 1):
        if intersection(p, q, a[i], a[i + 1]) == 1:
            return 1
    if intersection(p, q, a[0], a[-1]) == 1:
        return 1
    return 0
        
#Check do we need the square lx * ly with left-down in (x, y)
def good_square(x, y):
    if is_in(x, y) == 1 or is_in(x + lx, y) == 1 or is_in(x + lx, y + ly) == 1 or is_in(x, y + ly) == 1:
        return 1
    if inter(x, y, x + lx, y) == 1 or inter(x + lx, y, x + lx, y + ly) == 1 or inter(x + lx, y + ly, x, y + ly) == 1 or inter(x, y + ly, x, y) == 1:
        return 1
    return 0

#END OF GEOMETRY


#TSP SOLUTION

#Function of the state
def f_optimal(all_points):
    dist = 0
    for i in range(0, len(all_points) - 1):
        dist = dist + get_dist(all_points[i], all_points[i + 1])
    #dist = dist + get_dist(all_points[0], all_points[-1])
    dist = dist + get_dist(zero, all_points[0]) + get_dist(all_points[-1], zero)
    return dist

#Generation of the new state
def gen_pos():
    p1 = randint(0, len(all_points) - 1)
    p2 = randint(0, len(all_points) - 1)
    if p1 > p2:
        p1, p2 = p2, p1
    b = []
    for i in range(0, p1):
        b.append(all_points[i])
    for i in range(p1, p2 + 1):
        b.append(all_points[p2 - i + p1])
    for i in range(p2 + 1, len(all_points)):
        b.append(all_points[i])
    #print(b)
    #b[p1], b[p2] = b[p2], b[p1]
    #b = b[:p1] + b[p1 : (p2 + 1)] + b[(p2 + 1):]
    return b

#Solving TSP
def solve_TSP():
    global all_points
    #print(len(all_points))
    shuffle(all_points)
    cur_ans = f_optimal(all_points)
    t1 = 200 
    t2 = 0.00001
    while t1 > t2:
        #print(t1)
        p1 = randint(0, len(all_points) - 1)
        p2 = randint(0, len(all_points) - 1)
        if p1 > p2:
            p1, p2 = p2, p1
        newVal = cur_ans
        if p1 == 0:
            if p2 == len(all_points) - 1:
                newVal = cur_ans
            else:
                newVal = cur_ans - get_dist(all_points[p2], all_points[p2 + 1]) + get_dist(all_points[p1], all_points[p2 + 1]) - get_dist(zero, all_points[p1]) + get_dist(zero, all_points[p2])
        else:
            if p2 == len(all_points) - 1:
                newVal = cur_ans - get_dist(all_points[p1 - 1], all_points[p1]) + get_dist(all_points[p2], all_points[p1 - 1]) - get_dist(zero, all_points[p2]) + get_dist(zero, all_points[p1])
            else:
                newVal = cur_ans - get_dist(all_points[p1 - 1], all_points[p1]) + get_dist(all_points[p2], all_points[p1 - 1]) - get_dist(all_points[p2], all_points[p2 + 1]) + get_dist(all_points[p1], all_points[p2 + 1])
            
        #print(len(newPoints))
        opt = cur_ans - newVal
        if opt > 0 or random() < exp(min(opt / t1, 1)):
            cur_ans = newVal
            b = []
            for i in range(0, p1):
                b.append(all_points[i])
            for i in range(p1, p2 + 1):
                b.append(all_points[p2 - i + p1])
            for i in range(p2 + 1, len(all_points)):
                b.append(all_points[i])
            all_points = b.copy()
        #print(2)
        t1 *= 0.99998
    


#END OF TSP SOLUTION


#Solution for problem
def solve():
    global all_points
    all_points.clear()
    minx = 0
    miny = 0
    maxx = 0
    maxy = 0
    for point in a:
        minx = min(minx, point["x"])
        miny = min(miny, point["y"])
        maxx = max(maxx, point["x"])
        maxy = max(maxy, point["y"])
    k_up = int(max(0, maxy // ly + 1))
    k_down = int(max(0, -miny // ly + 1))
    k_left = int(max(0, -minx // lx + 1))
    k_right = int(max(0, maxx // lx + 1))
    print(k_up, k_down)
    if (k_up + k_down)*(k_left + k_right) > 50 * 50:
        return;
    for i in range(-k_left - 1, k_right + 1):
        for j in range(-k_down - 1, k_up + 1):
            if good_square(i * lx, j * ly) == 1:
                all_points.append({"x": i * lx + lx / 2, "y" : j * ly + ly / 2})
    print(all_points)
    solve_TSP()
    print(a)
    #print(all_points)
    
@app.route('/sort', methods = ['POST'])
def sort():
    global points 
    points = request.get_json()
    get_distance()
    pos = 0
    for i in range(0, len(a)):
        if a[i]["x"] < a[pos]["x"] or (a[i]["x"] == a[pos]["x"] and a[i]["y"] < a[pos]["y"]):
            pos = i
    a[pos], a[0] = a[0], a[pos]
    for j in range(0, len(a)):
        for i in range(1, len(a) - 1):
            if get_square(a[0], a[i], a[i + 1]) < 0 or (get_square(a[0], a[i], a[i + 1]) == 0 and get_dist(a[0], a[i]) > get_dist(a[0], a[i + 1])):
                a[i], a[i + 1] = a[i + 1], a[i]
    points1 = points.copy()
    print(a)
    for i in range(0, len(a)):
        points1[i] = points[a[i]["id"]]
    points = points1.copy()
    return jsonify(points)

def go_to_ok():
    global ans_points
    ans_points.clear()
    print(base)
    for i in range(0, len(all_points)):
        ans_points.append({"lat": all_points[i]["y"] / 1000 / dpy + base["lat"], "lng": all_points[i]["x"] / 1000 / dpx + base["lng"]})
    return 0
'''

@app.route('/sendHomePosition', methods = ['POST'])
def makeHome():
    location = request.get_json()
    main.get_dps(location)
    print(main.dpx, main.dpy)
    return jsonify(location)

@app.route('/send', methods = ['POST'])
def send():
    main.points = request.get_json()
    print(main.points)
    main.get_distance()
    main.solve() 
    
    print(main.a, main.dpx, main.dpy)
    print(main.lx, main.ly)
    print(main.all_points)
    return jsonify(main.ans_points)

@app.route('/sendInfo', methods = ['POST'])
def sendInfo():
    val = request.get_json()
    angle = val[0]
    height = val[1]
    ratio = val[2]
    ov_ratio = val[3];
    main.lx = (2 * height * tan(angle / 360 * 3.1415926))
    main.ly = main.lx / ratio
    main.lx *= (1 - ov_ratio)
    main.ly *= (1 - ov_ratio)
    print(main.lx, main.ly)
    return jsonify(main.lx)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

    