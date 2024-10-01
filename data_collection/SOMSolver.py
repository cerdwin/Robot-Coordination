#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import numpy as np
import time as tm

#import communication messages
from messages import *

################################################
# Animation during the computation (Disabled in BRUTE)
################################################
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch

animate = True

def plot_points(points, specs = 'r'):
    x_val = [x[0] for x in points]
    y_val = [x[1] for x in points]
    plt.plot(x_val, y_val, specs)

def plot_circle(xy, radius):
    ax = plt.gca()
    circle = Circle(xy, radius, facecolor = 'yellow',edgecolor = 'orange', 
        linewidth = 1, alpha = 0.2)
    ax.add_patch(circle)

def show_ring(solver, ring, color):
    plt.clf()
    plt.axis('equal')
    # show goals of the given TSP instance
    for goal in solver.goals:
        plot_circle(goal, solver.radius)
        plot_points([goal], 'ro')

    # show the final ring of the neurons (black)
    plot_points(ring, color)

    # highlight inhibited neurons with their associated goals (green)
    inhibited_neurons = solver.get_inhibited_neurons()
    for n in inhibited_neurons:
        plot_points([n.position], 'go')
        plot_points([n.position, solver.goals[n.goal_idx]], 'g--')
        plot_points([n.goal_position], 'rx')	

##################################################
# Neuron class
##################################################
class Neuron:
    def __init__(self):
        # neuron position
        self.position = np.array((0, 0))
        # associated goal position
        self.goal_position = np.array((None, None))
        # index of the goal which inhibited this neuron
        self.goal_idx = None
        pass

    def adapt_neuron(self, beta, goal):
        self.position[0] += beta * (goal[0] - self.position[0])
        self.position[1] += beta * (goal[1] - self.position[1])
        pass

    def update_goal_position(self, goal, radius):
        # TODO - replace this code by the altergnate goal position
        self.goal_position = goal

        return self.goal_position

##################################################
# SOMSolver class
##################################################
class SOMSolver:
    def __init__(self):
        self.goals = []
        self.radius = 0
        
        self.N = 0
        self.M = 0
        
        self.sigma = 12.41 * self.N + 0.6
        # faster version -- used only for UIR
        self.sigma = self.N
        self.mi = 0.5 # learning rate 
        self.alpha = 0.1 # gain decreasing rate

        self.neurons = [Neuron() for i in range(0, self.M)]

    def plan_tour(self, goals, radius=0):
        """ Method to plan the tour given set of goals and their neighborhood
        Args: goals - Pose[] - list of goal poses in world coordinates
              radius - float - size of the neighborhood in metres
        Returns: Path - the found tour
        """

        # vector containint coordinates of N goal cities
        self.goals = [(p.position.x, p.position.y) for p in goals]
        # size of the goal neighborhoods
        self.radius = radius 
        
        self.N = len(goals) # number of goals
        self.M = int(2.5 * self.N) # number of neurons
        
        # set the learning rate based on the neuron count N (original version)
        self.sigma = 12.41 * self.N + 0.6
        # faster version -- used only for UIR
        self.sigma = self.N
        self.mi = 0.5 # learning rate 
        self.alpha = 0.1 # gain decreasing rate

        # compute center and deviations of the goals
        np_goals = np.array([np.array(g) for g in self.goals])
        center = np.average(np_goals, axis=0)
        dev = np.std(np_goals, axis=0)
        
        # prepare matrix of the M neurons
        self.neurons = [Neuron() for i in range(0, self.M)]
        # initialize neurons by an ellipse
        for i in range(0, self.M):
            angle = (2 * math.pi * i) / self.M 
            direction = np.multiply([math.cos(angle), math.sin(angle)], dev)
            pos = center + direction
            self.neurons[i].position = pos

        # solve #################################################################
        # stopping criteria
        max_iterations = 120
        max_error = max(dev) * 1e-5

        start_time = tm.process_time()

        # start of the main cyclus	
        for epoch_idx in range(max_iterations):
            self.learn_epoch(epoch_idx)
            error = self.statistics(epoch_idx, start_time)
            if animate:
                show_ring(self, self.get_neurons_path(), 'kx-')
                plt.pause(0.03)
            if error < max_error:
                break

        path = self.reconstruct_path()
        tour = Path()
        for p in path:
            goal = Pose(Vector3(p[0],p[1],0),Quaternion(0,0,0,1))
            tour.poses.append(goal)

        return tour

    def select_winner(self, goal_idx):
        (act_goal_x, act_goal_y) = self.goals[goal_idx]

        best_idx = None

        for idx, neuron in enumerate(self.neurons):
            if neuron.goal_idx == None:
                # TODO - select the closest uninhibited neuron (best_idx)
                # use squared distance for a faster computation
                best_idx = idx

        self.neurons[best_idx].goal_idx = goal_idx		
        return best_idx

    def neighborhood_fce(self, distance):
        return math.exp(-distance * distance / self.sigma / self.sigma)

    def learn_epoch(self, learning_epoch):
        # clear values from the previous learning_epoch
        for n in self.neurons:
            n.goal_idx = self.gx = self.gy = None

        # chooce random order of the goals
        order = np.random.permutation(len(self.goals))

        # precompute betas for faster computation
        distances = range(int(-0.2*self.M)+1, int(0.2*self.M))
        betas = [self.mi*self.neighborhood_fce(dst) for dst in distances]

        # choose the closest neuron for each goal
        for goal_idx in order:
            act_goal = self.goals[goal_idx]
            winner_idx = self.select_winner(goal_idx)
            winner = self.neurons[winner_idx]
            alternate_goal = winner.update_goal_position(act_goal, self.radius)

            # TODO - update goal positions in the neighborhoods
            act_beta = 0.1
            winner.adapt_neuron(act_beta, alternate_goal)

        # update learing parameters
        self.sigma = (1 - self.alpha) * self.sigma	

    def reconstruct_path(self):
        inhibited_neurons = self.get_inhibited_neurons()
        path = [n.goal_position for n in inhibited_neurons]
        if len(path) > 0: 
            path = path + [path[0]]
        return path

    # save the best solution, print stats and return current error
    def statistics(self, iteration, start_time):        
        error_sq = 0
        for n in filter(lambda x : x.goal_idx != None, self.neurons):
            dx = n.position[0] - n.goal_position[0]
            dy = n.position[1] - n.goal_position[1]
            dst_sq = dx*dx + dy*dy
            error_sq = max(error_sq, dst_sq)
        error = math.sqrt(error_sq)

        duration = tm.process_time() - start_time
        print('iter {:3d}: error = {:11.6f}, time = {:6.3f} s'.format(
            iteration, error, duration))
        return error

    def get_neurons_path(self):
        path = [n.position for n in self.neurons]
        if len(path) > 0: 
            path = path + [path[0]]
        return path

    def get_inhibited_neurons(self):
        return [x for x in self.neurons if x.goal_idx != None]
    
