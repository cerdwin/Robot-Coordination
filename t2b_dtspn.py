#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch

#import communication messages
from messages import *

sys.path.append('dtspn')
sys.path.append('lkh')
sys.path.append('data_collection')

import DTSPNSolver as solver

################################################
# Final plotting (Used in BRUTE)
################################################
def plot_points(points, specs = 'b'):
    x_val = [x.x for x in points]
    y_val = [x.y for x in points]
    plt.plot(x_val, y_val, specs)

def plot_circle(xy, radius):
    ax = plt.gca()
    circle = Circle([xy.x, xy.y], radius, facecolor='yellow',edgecolor="orange", linewidth=1, alpha=0.2)
    ax.add_patch(circle)

def plot_map():
    """Draw the goal positions with neighborhood"""
    plt.clf()
    plt.axis('equal')
    plot_points(goals, 'ro')
    if sensing_radius != None:
        for goal in goals:
            plot_circle(goal, sensing_radius)

################################################
# Testing
################################################
#define planning problems:
    #  map file 
    #  minimum turning radius
    #  sensing radius
    #  solver type
scenarios = [
    ("./problems/mini3.txt", 0.5, 0.5, 'Decoupled'),
    ("./problems/burma14.txt", 0.5, 0.5, 'Decoupled'),
    
    ("./problems/mini3.txt", 0.5, 0.5, 'NoonBean'),
    ("./problems/burma14.txt", 0.5, 0.5, 'NoonBean'),
]

def load_map(file):
    goals = []
    with open(scenario[0]) as fp:
        for line in fp:
            label, x, y = line.split()
            goals.append(Vector3(float(x), float(y), 0))
    return goals

for scenario in scenarios:
    # Fix the problems
    random.seed(42)

    # read config with goal positions
    goals = load_map(scenario[0])
    radius = scenario[1]
    sensing_radius = scenario[2]
    solver_type = scenario[3]

    ######################################
    # plot arena and goals (and their neighborhoods)
    ######################################
    plot_map()
    plt.pause(0.1)

    ######################################
    #tour planning
    ######################################

    if solver_type == 'NoonBean':
        path, path_len = solver.plan_tour_noon_bean(goals, sensing_radius, radius)
    elif solver_type == 'Decoupled':
        path, path_len = solver.plan_tour_decoupled(goals, sensing_radius, radius)

    ######################################
    # plot result
    ######################################
    plot_points([p.position for p in path], 'b-')
    plt.pause(5)
