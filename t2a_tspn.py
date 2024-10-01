#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch

import sys
import os
import math
import numpy as np

sys.path.append('data_collection')

#import communication messages
from messages import *
 
#import SOM solver
import SOMSolver as som

################################################
# Final plotting (Used in BRUTE)
################################################
def plot_path(ax, path, clr="r"):
    """Draw the path"""
    length = 0
    if path is not None:
        poses = np.asarray([(pose.position.x,pose.position.y) for pose in path.poses])
        ax.plot(poses[:,0], poses[:,1], '.', color=clr)
        ax.plot(poses[:,0], poses[:,1], '-', color=clr)

def plot_goals(ax, goals, neighborhood_size):
    """Draw the goal positions with neighborhood"""
    for goal in goals:
        x = goal.position.x
        y = goal.position.y
        #plot the point
        ax.plot([x], [y], ".k", markersize=7)
        #plot the neighborhood
        if(neighborhood_size > 0):
            circle = Circle((x,y), neighborhood_size, facecolor="yellow",edgecolor="orange", linewidth=1, alpha=0.2)
            ax.add_patch(circle)

################################################
# Testing part
################################################
# 1) file with cities containing coordinates (idx, x, y) separated by new-line symbol
# 2) radius of the neighborhoods
dataset = [
    ("burma14", 0.0),
    ("burma14", 0.5),
    ("burma14", 1.0),

    ("att48", 0.0),
    ("att48", 200.0),
    ("att48", 500.0),
]

def load_problem(problem_file):
    """Load problem from file"""
    goals = []
    data = np.genfromtxt(problem_file)
    for goal in data:
        pose = Pose(Vector3(goal[1],goal[2],0), Quaternion(0,0,0,1))
        goals.append(pose)
    return goals

if __name__=="__main__":
    planner = som.SOMSolver()
    for problem, radius in dataset:
        problem_file = './problems/' + problem + '.txt'

        plt.figure(1)

        # load problem from a file
        goals = load_problem(problem_file)

        #calculate the tour
        print("Solving {}, radius = {} ----------- ".format(problem, radius))
        path = planner.plan_tour(goals, radius)

        #plot the scenario and path
        plt.clf()
        ax = plt.axes()
        plot_goals(ax, goals, radius)
        plot_path(ax, path, 'r')
        plt.xlabel('x[m]')
        plt.ylabel('y[m]')
        plt.axis('equal')
        plt.pause(1)
        # plt.show()
