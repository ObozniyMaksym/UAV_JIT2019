from app import app
import sys
from flask import jsonify, render_template, request, Response
from math import cos, sqrt, exp
from random import random, randint, shuffle
import json

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

#Transformation from lat/lng to cartesian coordinates
def get_distance():
    a.clear()
    phi = points[0]["lat"] / 180 * 3.1415926
    global dpx, dpy
    dpx = 111.321*cos(phi) - 0.0094*cos(3*phi)
    dpy = 111.143
    a.append({"x": 0, "y": 0, "id": 0})
    for i in range(1, len(points)):
        a.append({"x": (points[i]["lng"] - points[0]["lng"])*dpx*1000, "y": (points[i]["lat"] - points[0]["lat"])*dpy*1000, "id": i})

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
    dist = dist + get_dist(all_points[0], all_points[-1])
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
                newVal = cur_ans - get_dist(all_points[p2], all_points[p2 + 1]) + get_dist(all_points[p1], all_points[p2 + 1])
        else:
            if p2 == len(all_points) - 1:
                newVal = cur_ans - get_dist(all_points[p1 - 1], all_points[p1]) + get_dist(all_points[p2], all_points[p1 - 1])
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
    for i in range(-20, 21):
        for j in range(-20, 21):
            if good_square(i * lx, j * ly) == 1:
                all_points.append({"x": i * lx + lx / 2, "y" : j * ly + ly / 2})
    print(1)
    solve_TSP()
    print(a)
    print(all_points)
    
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
    for i in range(0, len(all_points)):
        ans_points.append({"lat": all_points[i]["y"] / 1000 / dpy + points[0]["lat"], "lng": all_points[i]["x"] / 1000 / dpx + points[0]["lng"]})
    return 0


@app.route('/send', methods = ['POST'])
def send():
    goo = 1
    global points
    points = request.get_json()
    #print(points)
    get_distance()
    solve()
    go_to_ok()
    global ans_points
    #print(ans_points)
    return jsonify(ans_points)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

    