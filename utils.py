"""
Author tlyman
COSI 217a Final Project
Fall 2021

holds the try mutate method among other things
"""

import numpy as np
from genome import Genome
import random
import pprint
import matplotlib.pyplot as plt

TOTAL_POP   = 1000

#try mutating each member of each genome
def tryMutate(genomes, data, gens, apex_list):
    
    for g in list(genomes.values()):

        for i in range(0, int(g.population * TOTAL_POP)):    
            
            mutated = Genome(g.memory, g.actions.copy(), 1/TOTAL_POP)
        
            #point mutation
            for a in range(0,len(mutated.actions)):
                if random.random() < 1/50000:
                    #print('POINT MUTATION')
                    mutated.actions[a] = 1 - mutated.actions[a]
                    #print(g.toString(), ' -> ', mutated.toString())
             
            #duplication
            if random.random() < 1/(100000) and g.memory < 4:
                #print('DUPE MUTATION')
                mutated.actions.extend(mutated.actions.copy())
                mutated.memory += 1
                #print(g.toString(), ' -> ', mutated.toString())
            
            #split
            if random.random() < g.memory/100000 and g.memory > 1:
                #print('SPLIT MUTATION')
                middle = int(len(mutated.actions)/2)
                if random.random() < 0.5:
                    mutated.actions = mutated.actions[:middle]
                else:
                    mutated.actions = mutated.actions[middle:]
                mutated.memory -= 1
                
               
            #print('before check: ', g.toString())
               
            #check if mutation occurred, create or add to new species    
            if not g.equals(mutated):
                #print(g.toString(), ' -> ', mutated.toString())
                g.population -= 1/TOTAL_POP
                matched = False
                
                for other_g in genomes.values():
                    if other_g.equals(mutated):
                        matched = True
                        other_g.population += 1/TOTAL_POP
                        
                #create entry in dictionaries for new genome
                if (not matched): #and (not mutated.toString() == '00010001'):
                    genomes[mutated.toString()] = mutated
                    
                    if not mutated.toString() in data.keys():
                        data[mutated.toString()] = [0]*gens
                        apex_list[mutated.toString()] = 0
                        
    return genomes, data, apex_list
                        
                    
            
def plotResults(data, gens, apex_list):
    
    x = np.arange(gens)
    plots = list(data.values())
    names = list(data.keys())
    
    plt.xlabel("Generation")
    plt.ylabel("Percentage of Population")
    plt.figure(figsize=(60,3))
    for key, d in data.items():
        if apex_list[key] == 1:
            plt.plot(x, d, label = key)
    plt.legend()
    plt.show()
    
    return




