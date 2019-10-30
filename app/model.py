from app import app
import sys
from flask import jsonify, render_template, request, Response
from math import cos, sqrt, exp, tan
from random import random, randint, shuffle
import json

class Geometry():
        #Distance between 2 points
    def get_dist(self, a, b):
        return sqrt((a["x"] - b["x"]) * (a["x"] - b["x"]) + (a["y"] - b["y"]) * (a["y"] - b["y"]))

    #Oriented square of triangle
    def get_square(self, a, b, c):
        return (a["x"] - b["x"]) * (a["y"] + b["y"]) + (b["x"] - c["x"]) * (b["y"] + c["y"]) + (c["x"] - a["x"]) * (c["y"] + a["y"])
    
    #Check do the segments intersect
    def intersection(self, a, b, c, d):
        if self.get_square(a, c, b) * self.get_square(a, d, b) < 0 and self.get_square(c, a, d) * self.get_square(c, b, d) < 0:
            return 1
        return 0

    #Check do the segment and the border intersect
    def inter(self, x1, y1, x2, y2):
        p = {"x": x1, "y": y1}
        q = {"x": x2, "y": y2}
        for i in range(0, len(self.a) - 1):
            if self.intersection(p, q, self.a[i], self.a[i + 1]) == 1:
                return 1
        if self.intersection(p, q, self.a[0], self.a[-1]) == 1:
            return 1
        return 0
    
class DroneThirdAlgo(Geometry):
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
    #Get dpx and dpy
    def get_dps(self, location):
        self.base = location
        phi = self.base["lat"] / 180 * 3.1415926
        self.dpx = 111.321*cos(phi) - 0.0094*cos(3*phi)
        self.dpy = 111.143

    #Transformation from lat/lng to cartesian coordinates
    def get_distance(self):
        self.a.clear()
        for i in range(0, len(self.points)):
            self.a.append({"x": (self.points[i]["lng"] - self.base["lng"])*self.dpx*1000, "y": (self.points[i]["lat"] - self.base["lat"])*self.dpy*1000, "id": i})

    
    #Check is the point inside the border
    def is_in(self, x, y):
        p = {"x": x, "y": y}
        q = {"x": 1000000000, "y": 970005041}
        kol = 0
        for i in range(0, len(self.a) - 1):
            if self.intersection(p, q, self.a[i], self.a[i + 1]) == 1:
                kol = kol + 1
        if self.intersection(p, q, self.a[0], self.a[-1]) == 1:
            kol = kol + 1
        if kol % 2 == 1:
            return 1
        return 0
    
    #Check do we need the square lx * ly with left-down in (x, y)
    def good_square(self, x, y):
        if self.is_in(x, y) == 1 or self.is_in(x + self.lx, y) == 1 or self.is_in(x + self.lx, y + self.ly) == 1 or self.is_in(x, y + self.ly) == 1:
            return 1
        if self.inter(x, y, x + self.lx, y) == 1 or self.inter(x + self.lx, y, x + self.lx, y + self.ly) == 1 or self.inter(x + self.lx, y + self.ly, x, y + self.ly) == 1 or self.inter(x, y + self.ly, x, y) == 1:
            return 1
        return 0

    #END OF GEOMETRY


    #TSP SOLUTION

    #Function of the state
    def f_optimal(self, all_points):
        dist = 0
        for i in range(0, len(all_points) - 1):
            dist = dist + self.get_dist(all_points[i], all_points[i + 1])
        #dist = dist + get_dist(all_points[0], all_points[-1])
        dist = dist + self.get_dist(self.zero, all_points[0]) + self.get_dist(all_points[-1], self.zero)
        return dist

    #Solving TSP
    def solve_TSP(self):
        shuffle(self.all_points)
        cur_ans = self.f_optimal(self.all_points)
        t1 = 200 
        t2 = 0.00001
        while t1 > t2:
            p1 = randint(0, len(self.all_points) - 1)
            p2 = randint(0, len(self.all_points) - 1)
            if p1 > p2:
                p1, p2 = p2, p1
            newVal = cur_ans
            if p1 == 0:
                if p2 == len(self.all_points) - 1:
                    newVal = cur_ans
                else:
                    newVal = cur_ans - self.get_dist(self.all_points[p2], self.all_points[p2 + 1]) + self.get_dist(self.all_points[p1], self.all_points[p2 + 1]) - self.get_dist(self.zero, self.all_points[p1]) + self.get_dist(self.zero, self.all_points[p2])
            else:
                if p2 == len(self.all_points) - 1:
                    newVal = cur_ans - self.get_dist(self.all_points[p1 - 1], self.all_points[p1]) + self.get_dist(self.all_points[p2], self.all_points[p1 - 1]) - self.get_dist(self.zero, self.all_points[p2]) + self.get_dist(self.zero, self.all_points[p1])
                else:
                    newVal = cur_ans - self.get_dist(self.all_points[p1 - 1], self.all_points[p1]) + self.get_dist(self.all_points[p2], self.all_points[p1 - 1]) - self.get_dist(self.all_points[p2], self.all_points[p2 + 1]) + self.get_dist(self.all_points[p1], self.all_points[p2 + 1])
            
            opt = cur_ans - newVal
            if opt > 0 or random() < exp(min(opt / t1, 1)):
                cur_ans = newVal
                b = []
                for i in range(0, p1):
                    b.append(self.all_points[i])
                for i in range(p1, p2 + 1):
                    b.append(self.all_points[p2 - i + p1])
                for i in range(p2 + 1, len(self.all_points)):
                    b.append(self.all_points[i])
                self.all_points = b.copy()
            t1 *= 0.99998
        self.cur_ans = cur_ans

    #END OF TSP SOLUTION

    #Solution for problem
    def solve(self):
        self.all_points.clear()
        minx = 0
        miny = 0
        maxx = 0
        maxy = 0
        for point in self.a:
            minx = min(minx, point["x"])
            miny = min(miny, point["y"])
            maxx = max(maxx, point["x"])
            maxy = max(maxy, point["y"])
        k_up = int(max(0, maxy // self.ly + 1))
        k_down = int(max(0, -miny // self.ly + 1))
        k_left = int(max(0, -minx // self.lx + 1))
        k_right = int(max(0, maxx // self.lx + 1))
        if (k_up + k_down)*(k_left + k_right) > 50 * 50:
            return;
        for i in range(-k_left - 1, k_right + 1):
            for j in range(-k_down - 1, k_up + 1):
                if self.good_square(i * self.lx, j * self.ly) == 1:
                    self.all_points.append({"x": i * self.lx + self.lx / 2, "y" : j * self.ly + self.ly / 2})
        self.solve_TSP()
        self.ans_points.clear()
        print('11')
        print(self.all_points)
        self.all_points.insert(0, self.zero)
        self.all_points.append(self.zero)
        for i in range(0, len(self.all_points)):
            self.ans_points.append({"lat": self.all_points[i]["y"] / 1000 / self.dpy + self.base["lat"], "lng": self.all_points[i]["x"] / 1000 / self.dpx + self.base["lng"]})
        return self.ans_points;
    
  

    