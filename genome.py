"""
Author tlyman
COSI 217a Final Project
Fall 2021

holds the genome class
"""

import numpy as np
import random
import pprint

class Genome:
    
    memory = 0
    actions = []
    hist = []
    population = 0.0
    score = 0
     
    # m = memory     (int number of moves remembered)
    # a = actions    (array of actions where genbome does actions[i] when history = i)
    # p = population (float fraction of individuals of this genome)
    # hist           (array of previous moves)
    # fitness        (float average fitness)
    def __init__(self, m, a, p):
        self.memory = m
        self.actions = a
        self.hist = [1]*m
        self.score = 0
        self.population = p
        
    
    #check if two genomes are the same
    # G = genome to compare with
    def equals(self, G):
        return np.array_equal(self.actions, G.actions)
    
    
    def toString(self):
        s = ""
        for a in self.actions:
            if a == 1:
                s = s + "1"
            else:
                s = s + "0"
        return s
    
    
    #add most recent move(s) to history
    # opp = opponent's newest move, either 0 or 1
    # play = player's newest move, either 0 or 1
    def update(self, play, opp):
        if self.memory > 1:
            self.hist    = [self.hist[-1]] + self.hist[:-1]
            self.hist    = [self.hist[-1]] + self.hist[:-1]
            self.hist[1] = play
            
        self.hist[0] = opp


    #return decimal version of history (indicates genome index)
    def getIndex(self):
        return sum(val*(2**idx) for idx, val in enumerate(reversed(self.hist)))
        
    
    #do the action for the specified index (returns 0/1), includes noise
    def action(self, index):
        a = self.actions[index]
        if random.random() < self.memory/(200):
            return 1-a
        else:
            return a