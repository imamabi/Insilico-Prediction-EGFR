#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 00:02:26 2023

@author: ibrahimimam
"""
#A python script to perfom enrichment plot and calculate AUC

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# load docking results into a pandas dataframe
df = pd.read_csv('sorted_results', sep= '\t')

percentages = [1,5,10,100]

for percent in percentages:
    docking_results = df[:(int(np.ceil(len(df) * ((percent/100)))))]
    
    activity = docking_results['Ligand'].str.split('_', n=2, expand = True)
    
    docking_results['activity'] = activity[1]
    
    
    #A function that will convert activity to binary decisions
    def modify_column(x):
        if x == 'active':
            return (int(1))
        else:
            return 0
    
    docking_results['true_active']= docking_results['activity'].apply(modify_column)
    
    total_db = docking_results['true_active']
    
    total_count = len(docking_results['true_active'])
    active_count = docking_results['true_active'].sum()
    
    
    percent_active = []
    percent_sorted = []
    percent_decoy= []
    
    current_active = 0
    current_tcount = 0
    current_decoy = 0
    
    for ligand in total_db:
        current_active = current_active + ligand
        current_tcount = current_tcount + 1
        if ligand == 0:
            current_decoy = current_decoy + 1
        
        percent_act = float(current_active) / active_count * 100
        percent_sort = float(current_tcount) / total_count * 100
        percent_d = float(current_decoy) / (total_count - active_count) * 100
        
        
        percent_active.append(percent_act)
        percent_sorted.append(percent_sort)
        percent_decoy.append(percent_d)
        
    enrichment = [percent_sorted, percent_active]
    enrichment2 = [percent_decoy,percent_active]
    
    #caluclating AUC for the selected model
    x = np.array(enrichment2[0])/100
    y = np.array(enrichment2[1])/100
    currentp = 0
    auc = 0
    rangeX = len(x)-1
    added = 0
    for i in range (rangeX):
        currentp = y[i]*(x[i+1]-x[i])
        added = (y[i+1] - y[i])*(x[i+1]-x[i])
        auc = auc + currentp + added
    print (f"AUC: %.3f" % auc)
    
    # plot the enrichment ROC for model 1
    # plot the enrichment factor as a function of the percentage of the ranked list considered
    plt.title('Enrichment curve')
    plt.xlabel('% sorted of database')
    plt.ylabel('% ligand of found')
    plt.plot(enrichment[0],enrichment[1],label=f'{percent}percent AUC= %0.3f'%auc)
    plt.plot([0,100],[0,100], 'r:')
    plt.ylim(ymin=0)
    plt.xlim(xmin=0)
    plt.legend(loc='upper left')
    plt.savefig(f'Enrichment_{percent}%_ROCs.png')
