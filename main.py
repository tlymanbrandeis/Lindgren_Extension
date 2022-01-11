"""
Author tlyman
COSI 217a Final Project
Fall 2021

main file for running simulation
"""

from genome import Genome
from utils import tryMutate, plotResults
import numpy as np
import random
import itertools

PAYOUT      = np.array([[1, 5], [0, 3]])
GENERATIONS = 100001
ROUNDS      = 500
TOTAL_POP   = 1000
GROWTH      = 0.1

genomes = {
    "00": Genome(1, [0, 0], 1/4),
    "01": Genome(1, [0, 1], 1/4),
    "10": Genome(1, [1, 0], 1/4),
    "11": Genome(1, [1, 1], 1/4)
}

#DICTIONARY OF STUFF TO PLOT
data = {
    #"number of genomes": [],
    #"average score": [],
    "00": [0]*GENERATIONS,
    "01": [0]*GENERATIONS,
    "10": [0]*GENERATIONS,
    "11": [0]*GENERATIONS  
}

#Keep track of which genomes are the most popular at some point (for plotting simplicity)
apex_list = {
    "00": 0,
    "01": 0,
    "10": 0,
    "11": 0  
}
    
    
#plays all combinations of genomes (including themselves)
#INPUT:
# agents - list of players
# p1_idx, p2_idx - index of each player in agents
def allPlayAll(agents, p1_idx, p2_idx):
    
    player1 = agents[p1_idx]
    player2 = agents[p2_idx]
    
    #print('{0}   vs   {1}'.format(player1.toString(), player2.toString()))

    p1_score, p2_score = game(player1, player2)

    #DONT ADD BOTH IF IDENTICAL
    player1.score += p1_score * (player2.population)
    if not player1.equals(player2):
        player2.score += p2_score * (player1.population)
    
    #print('{0}     {1}'.format(p1_score, p2_score))
    
    
    if p2_idx + 1 == len(agents):
        if p1_idx + 1 < len(agents):
            allPlayAll(agents, p1_idx + 1, p1_idx + 1)
        else:
            return
    else:
        allPlayAll(agents, p1_idx, p2_idx + 1)
        
        
        
#plays two Genomes against each other in iterated prisoners dilemma
#INPUT:  player1, player2 - genome objects representing competitors
#OUTPUT: average points per round for each player
def game(player1, player2):
    
    player1.hist = [1]*(player1.memory)
    player2.hist = [1]*(player2.memory)
    p1_score = 0
    p2_score = 0
    
    for r in range(ROUNDS):
        
        #do the round and log what was played
        p1_move = player1.action(player1.getIndex())
        p2_move = player2.action(player2.getIndex())
        
        #update each player's memory
        player1.update(p1_move, p2_move)
        player2.update(p2_move, p1_move)
        
        #figure out how points are distributed
        p1_score += PAYOUT[p1_move, p2_move]
        p2_score += PAYOUT[p2_move, p1_move]
    
    return p1_score/ROUNDS, p2_score/ROUNDS



#adjust all genome populations according to their relative fitness
def updatePop(agents):
    
    new_pops = []*len(agents)
    
    for agent in agents:
        d_si_x = GROWTH * agent.score * agent.population
        parens = 1.0
        
        for opponent in agents:
            parens -= (opponent.score * opponent.population) / agent.score
        new_pops.append(agent.population + (d_si_x * parens))
            
        #print(agent.toString(), 'score = {0:4.2f}'.format(agent.score))
            
    for (agent, new_pop) in zip(agents, new_pops):
         agent.population = new_pop
        
        
 #remove the dead genome and renormalize populations by evenly distributing the dead population's remains       
def genomeDeath(dead_agent, agents):
    
    share = dead_agent.population/(len(agents)-1)
    
    dead_agent.population = 0.0
    agents.remove(dead_agent)
    genomes.pop(dead_agent.toString(), None)
    
    for agent in agents:
        agent.population += share
    return agents
            
      

#iterate over generations
for i in range(GENERATIONS):
    if i % 50 == 0:
        print(' ')
        print('GENERATION ', i)
    
    agents = list(genomes.values())
    largest_agent = agents[0]
    second_largest = agents[0]
    
    for agent in agents:
        
        #check if any genomes have died out, otherwise reset them
        if agent.population < 1/TOTAL_POP:
            agents = genomeDeath(agent, agents)
        elif i % 50 == 0:
            print(agent.toString(), ' = {0:6.2f}%'.format(agent.population*100))
        agent.score = 0.0
        
        #identify the most popular strategy
        data[agent.toString()][i] = agent.population
        if agent.population >= largest_agent.population:
            largest_agent = agent
        elif agent.population >= second_largest.population:
            second_largest = agent
 
            
    apex_list[largest_agent.toString()] = 1
    apex_list[second_largest.toString()] = 1
    
    allPlayAll(agents, 0, 0)
    updatePop(agents)
    genomes, data, apex_list = tryMutate(genomes, data, GENERATIONS, apex_list)
        
plotResults(data, GENERATIONS, apex_list)        
        
    