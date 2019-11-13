import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import json
import math
import re
import csv
import scipy.stats as scp_stats
import scikit_posthocs as sp
from statannot import add_stat_annotation

#plt.rc('text', usetex=True)
#plt.rc('font', family='serif',size ='16')
pd.options.display.max_rows = 4000
#matplotlib.rcParams['ps.useafm'] = True
#matplotlib.rcParams['text.usetex'] = True

#mainFolder: main folder containing experiment folders
#folder: the folder header
#rep: number of repetitions
def minGenerationCount(mainFolder,folder,rep):
    minimum = 100000
    genCount= []
    for i in range(0,rep):
        csv_file = open('./'+mainFolder+'/'+folder+'xL/'+str(i+1)+'/log/evolution.txt')
        csv_reader = csv.reader(csv_file,delimiter='-')
        #line_count = 0
        #for row in csv_reader:
        #    line_count = line_count + 1
        rows = list(csv_reader)
        line_count = len(rows)
        genCount.append(line_count)
        #print(line_count)
    for count in genCount:
        if (count<=minimum):
            minimum = count
    #print(minimum)
    return minimum

#mainFolder: main folder containing experiment folders
#folder: array of folder headers
#tp: the type of graph 'evol','nModules','brokenConn'
#rep: number of repetitions
#indiv: boolean plot individual graphs or all in the same
#saveFile: name of the file in which the graph is saved
def plotResultGraphs(mainFolder,folders,tp,rep,indiv,saveFile):
    logCol = 1
    file ='evolution'
    if(tp=='evol'):
        logCol = 1
        file = 'evolution'
    elif (tp=='nModules'):
        logCol = 2
        file = 'bestFeatures'
    elif (tp=='brokenConn'):
        logCol = 11
        file = 'meanFeatures'
    
    if(not indiv):
        fig = plt.figure(figsize=(15,10))
        ax1 = fig.gca()
        
    for k in range(0,len(folders)):
        if(indiv):
            fig = plt.figure()
            ax1 = fig.gca()
        nGenerations = minGenerationCount(mainFolder,folders[k],rep)
        df = pd.DataFrame(columns=range(0,nGenerations))
        
        evolBest = []
        
        for i in range(0,rep):
            evolBest.clear()
            csv_file = open('./'+mainFolder+'/'+folders[k]+'xL/'+str(i+1)+'/log/'+file+'.txt')
            #csv_file = open('./filesFromLenghtExperiment/'+folders[k]+'xL/'+str(i+1)+'/log/bestFeatures.txt')
            #csv_file = open('/content/drive/My Drive/2019/Papers/Base Length/filesFromLenghtExperiment/'+folders[k]+'xL/'+str(i+1)+'/log/evolution.txt')
            csv_reader = csv.reader(csv_file,delimiter='-')
            line_count = 0
            for row in csv_reader:
                evolBest.append(float(row[logCol]))
                #evolBest.append(float(row[2]))
                line_count =line_count + 1
                #print(line_count)
                #print(evolBest)
                if line_count >= nGenerations:
                    break
            df.loc[i] = evolBest[:]

        #ax1.plot(df.min(),label='Best')
        #ax1.plot(df.max(),label='Worst')
        x = range(nGenerations)
        q3 = df.quantile(0.75)
        q1 = df.quantile(0.25)

        ax1.plot(x,df.median(),label='Median'+folders[k])
        if(indiv):
            ax1.plot(x,q3, color='k', linestyle='--',label='IQR')
        else:
            ax1.plot(x,q3, color='k', linestyle='--',label='_nolegend_')
        ax1.plot(x,q1, color='k', linestyle='--',label='_nolegend_')
        #ax1.fill_between(x, q1, q3, alpha=0.5)
        
        #plt.axhline(y=0.3, color='k', linestyle='-.')
        if(tp=='evol'):
            ax1.set_ylim(-0.1,6)
        elif(tp=='nModules'):
            ax1.set_ylim(-0.1,20)
        elif(tp=='brokenConn'):
            ax1.set_ylim(-0.1,4)
        ax1.legend()
        ax1.set_title('Length x'+folders[k])
        #ax1.set_xticks([0,100,200,300])
        #ax1.set_xticklabels(['0','3000','6000','9000'])
        ax1.set_xlabel('Generations')
        ax1.set_ylabel('Fitness')
        if(indiv):
        	plt.savefig(saveFile+folders[k]+'xL'+tp+'plot.eps',bbox_inches="tight")
    if(not indiv):
    	plt.savefig(saveFile+'xL'+tp+'plot.eps',bbox_inches="tight")
    plt.show()

#mainFolder: main folder containing experiment folders
#folder: array of folder headers
#tp: the type of graph 'evol','nModules','brokenConn'
#rep: number of repetitions
#indiv: boolean plot individual graphs or all in the same
#nEval: number of evaluations
#saveFile: name of the file in which the graph is saved
def plotResultGraphsEval(mainFolder,folders,tp,rep,indiv,nEval,saveFile):
    logCol = 1
    file ='evolution'
    if(tp=='evol'):
        logCol = 1
        file = 'evolution'
    elif (tp=='nModules'):
        logCol = 2
        file = 'bestFeatures'
    elif (tp=='brokenConn'):
        logCol = 11
        file = 'meanFeatures'
    
    if(not indiv):
        fig = plt.figure(figsize=(15,10))
        ax1 = fig.gca()
        
    for k in range(0,len(folders)):
        if(indiv):
            fig = plt.figure()
            ax1 = fig.gca()
        df = pd.DataFrame(columns=range(0,nEval))
        
        evolBest = []
        
        for i in range(0,rep):
            evolBest.clear()
            csv_file = open('./'+mainFolder+'/'+folders[k]+'xL/'+str(i+1)+'/log/'+file+'.txt')
            #csv_file = open('./filesFromLenghtExperiment/'+folders[k]+'xL/'+str(i+1)+'/log/bestFeatures.txt')
            #csv_file = open('/content/drive/My Drive/2019/Papers/Base Length/filesFromLenghtExperiment/'+folders[k]+'xL/'+str(i+1)+'/log/evolution.txt')
            csv_reader = csv.reader(csv_file,delimiter='-')
            rows = list(csv_reader)
            evaluationsPerGen = math.floor(nEval/len(rows))
            #print(evaluationsPerGen,len(rows))
            line_count = 0
            for row in rows:
            	value = float(row[logCol])
            	for l in range(0,evaluationsPerGen):
            		evolBest.append(value)
            #print(len(evolBest))
            if(len(evolBest)<nEval):
            	diff = nEval - len(evolBest)
            	for l in range(0,diff):
            		evolBest.append(value)
            #print(len(evolBest))
            df.loc[i] = evolBest[:]

        #ax1.plot(df.min(),label='Best')
        #ax1.plot(df.max(),label='Worst')
        x = range(nEval)
        q3 = df.quantile(0.75)
        q1 = df.quantile(0.25)

        ax1.plot(x,df.median(),label='Median'+folders[k])
        if(indiv):
            ax1.plot(x,q3, color='k', linestyle='--',label='IQR')
        else:
            ax1.plot(x,q3, color='k', linestyle='--',label='_nolegend_')
        ax1.plot(x,q1, color='k', linestyle='--',label='_nolegend_')
        ax1.fill_between(x, q1, q3, alpha=0.5)
        
        #plt.axhline(y=0.3, color='k', linestyle='-.')
        if(tp=='evol'):
            ax1.set_ylim(-0.1,6)
        elif(tp=='nModules'):
            ax1.set_ylim(-0.1,20)
        elif(tp=='brokenConn'):
            ax1.set_ylim(-0.1,4)
        ax1.legend()
        ax1.set_title('Length x'+folders[k])
        #ax1.set_xticks([0,100,200,300])
        #ax1.set_xticklabels(['0','3000','6000','9000'])
        ax1.set_xlabel('Fitness Evaluations')
        ax1.set_ylabel('Fitness')
        #plt.savefig('CPGGenDEOne.eps',bbox_inches="tight")
        if(indiv):
        	plt.savefig('./individualGraphs/'+saveFile+folders[k]+'xL'+tp+'plot.eps',bbox_inches="tight")
    if(not indiv):
    	plt.savefig(saveFile+tp+'plot.png',bbox_inches="tight")
    plt.show()
    
    
#mainFolder: main folder containing experiment folders
#folder: array of folder headers
#tp: the type of graph 'evol','nModules','brokenConn'
#rep: number of repetitions
#indiv: boolean plot individual graphs or all in the same 
#lastGen: plot only lastGen data or all data
#plotType: type of data plot (box,swarm,strip,violin)
#saveFile: name of the file in which the graph is saved
def boxplotResults(mainFolder,folders,tp,rep,indiv,lastGen,plotType,saveFile):
    logCol = 1
    file ='evolution'
    if(tp=='evol'):
        logCol = 1
        file = 'evolution'
        variable = 'Fitness'
    elif (tp=='nModules'):
        logCol = 2
        file = 'bestFeatures'
        variable = 'nModules'
    elif (tp=='brokenConn'):
        logCol = 11
        file = 'meanFeatures'
        variable = 'brokenConn'
    elif (tp=='nConn'):
        logCol = 19
        file = 'bestFeatures'
        variable = 'nConn'
        
    #dfAll = pd.DataFrame(columns=folders)
    dfAll = pd.DataFrame()
    
    if(not indiv):
        fig = plt.figure(figsize=(15,10))
        ax1 = fig.gca()
        
    
    data = []
        
    for k in range(0,len(folders)):
        if(indiv):
            fig = plt.figure()
            ax1 = fig.gca()
        #nGenerations = minGenerationCount(mainFolder,folders[k],rep)
        data.clear()
        
        for i in range(0,rep):
            csv_file = open('./'+mainFolder+'/'+folders[k]+'xL/'+str(i+1)+'/log/'+file+'.txt')
            csv_reader = csv.reader(csv_file,delimiter='-')
            rows = list(csv_reader)
            #print(rows)
            #print(nGenerations)
            if(lastGen):
                data.append(float(rows[-1][logCol]))
            else:
                line_count = 0
                for row in rows:
                    #print(row[logCol])
                    data.append(float(row[logCol]))
                    line_count =line_count + 1
                    #if line_count >= nGenerations:
                    #    break
                        
        dfPartial = pd.DataFrame(data,columns=[variable])
        dfPartial['Length'] = folders[k]
        #print(dfPartial)
        
        dfAll = dfAll.append(dfPartial,ignore_index=True)
        #ax1.set_title('Length x'+folders[k])
        #print(dfAll)
    #print(dfAll)
    #dfAll.boxplot(column='Fitness',by='Length',ax=ax1,grid=False,notch=False)
    #dfAll.groupby('Length',sort=True).boxplot()
    #if(tp=='evol'):
    #        ax1.set_ylim(-0.1,11)
    x = "Length"
    y = variable
    order = folders
    if(plotType=='box'):
        #ax = sns.boxplot(data=dfAll, x=x, y=y,order=order,showfliers=False)
        ax = sns.boxplot(data=dfAll, x=x, y=y,order=order)
    elif(plotType=='swarm'):
        ax = sns.swarmplot(data=dfAll, x=x, y=y,order=order)
    elif(plotType=='strip'):
        ax = sns.stripplot(data=dfAll, x=x, y=y,order=order)
    elif(plotType=='violin'):
        ax = sns.violinplot(data=dfAll, x=x, y=y,order=order)
    
    if(tp!='brokenConn'):
        add_stat_annotation(ax, data=dfAll, x=x, y=y, order=order, box_pairs=[("2","4")], test='Mann-Whitney', text_format='star', loc='outside',verbose=2)
    
    plt.savefig(saveFile+tp+plotType+'.eps',bbox_inches="tight")
    plt.show()
    print(scp_stats.kruskal(*[group[variable].values for name,group in dfAll.groupby('Length')]))
    
    #Connover
    #postHoc = sp.posthoc_conover(dfAll,val_col='Fitness',group_col='Length')
    #print(postHoc)
    if(tp!='brokenConn'):
        #Mann-Whitney
        postHoc = sp.posthoc_mannwhitney(dfAll,val_col=variable,group_col='Length')
        #print(postHoc)
        heatmap_args = {'linewidths': 0.25, 'linecolor': '0.5', 'clip_on': False, 'square': True, 'cbar_ax_bbox': [0.80, 0.35, 0.04, 0.3]}
        sp.sign_plot(postHoc, **heatmap_args)
    
    
    
#mainFolder: array of main folder containing experiment folders
#folder: array of folder headers
#tp: the type of graph 'evol','nModules','brokenConn','nModulesBase','brokenConnBase','evolBase'
#rep: number of repetitions  
#lastGen: plot only lastGen data or all data
#plotType: type of data plot (box,swarm,strip,violin)
def compareBases(mainFolders,folders,tp,rep,lastGen,plotType):
    logCol = 1
    file ='evolution'

    if((tp == 'evol') or (tp == 'evolBase')):
        logCol = 1
        file = 'evolution'
        variable = 'Fitness'
    elif ((tp=='nModules') or (tp == 'nModulesBase')):
        logCol = 2
        file = 'bestFeatures'
        variable = 'nModules'
    elif ((tp=='brokenConn') or (tp == 'brokenConnBase')):
        logCol = 11
        file = 'meanFeatures'
        variable = 'brokenConn'
        
    dfAll = pd.DataFrame()
    data = []
    
    
    
    for l in range(0,len(mainFolders)):
        dfBase = pd.DataFrame()
        for k in range(0,len(folders)):
            #nGenerations = minGenerationCount(mainFolders[l],folders[k],rep)
            data.clear()
        
            for i in range(0,rep):
                csv_file = open('./'+mainFolders[l]+'/'+folders[k]+'xL/'+str(i+1)+'/log/'+file+'.txt')
                csv_reader = csv.reader(csv_file,delimiter='-')
                rows = list(csv_reader)
                #print(rows)
                #print(nGenerations)
                if(lastGen):
                    data.append(float(rows[-1][logCol]))
                else:
                    line_count = 0
                    for row in rows:
                        #print(row[logCol])
                        data.append(float(row[logCol]))
                        line_count =line_count + 1
                        #if line_count >= nGenerations:
                        #    break

            dfPartial = pd.DataFrame(data,columns=[variable])
            dfPartial['Length'] = folders[k]
            #print(dfPartial)
        
            dfBase= dfBase.append(dfPartial,ignore_index=True)
            #ax1.set_title('Length x'+folders[k])
        dfBase['Base']=mainFolders[l]
        dfAll = dfAll.append(dfBase,ignore_index=True)
        #print(dfAll)
        #dfAll.boxplot(column='Fitness',by='Length',ax=ax1,grid=False,notch=False)
        #dfAll.groupby('Length',sort=True).boxplot()
    #print(dfAll)
    
    #print([group['Fitness'].values for name,group in dfAll.groupby(['Length','Base'])])
    if((tp!='nModulesBase') and (tp!='brokenConnBase') and (tp!='evolBase')):
        print(scp_stats.kruskal(*[group[variable].values for name,group in dfAll.groupby(['Length','Base'])]))
    else:
        print(scp_stats.kruskal(*[group[variable].values for name,group in dfAll.groupby(['Base'])]))


    if((tp!='brokenConn') and (tp!='nModulesBase') and (tp!='brokenConnBase') and (tp!='evolBase')):
        #Connover
        postHoc = sp.posthoc_conover([group[variable].values for name,group in dfAll.groupby(['Length','Base'])])
        #print(postHoc)
    
        #Mann-Whitney    
        #postHoc = sp.posthoc_mannwhitney([group['Fitness'].values for name,group in dfAll.groupby(['Length','Base'])])
        #print(postHoc)
    
        heatmap_args = {'linewidths': 0.25, 'linecolor': '0.5', 'clip_on': False, 'square': True, 'cbar_ax_bbox': [0.80, 0.35, 0.04, 0.3]}
        sp.sign_plot(postHoc, **heatmap_args)
    
    fig = plt.figure(figsize=(15,10))
    y = variable
    

    if((tp == 'nModulesBase') or (tp == 'brokenConnBase') or (tp == 'evolBase')):
        x = 'Base'
        order = mainFolders
        if(plotType=='box'):
            ax = sns.boxplot(data=dfAll, x=x, y=y,order=order)
        elif(plotType=='swarm'):
            ax = sns.swarmplot(data=dfAll, x=x, y=y,order=order)
        elif(plotType=='strip'):
            ax = sns.stripplot(data=dfAll, x=x, y=y,order=order)
        elif(plotType=='violin'):
            ax = sns.violinplot(data=dfAll, x=x, y=y,order=order)
    else:
        x = "Length"
        hue = "Base"
        order = folders
        if(plotType=='box'):
            ax = sns.boxplot(data=dfAll, x=x, y=y,order=order,hue = hue)
        elif(plotType=='swarm'):
            ax = sns.swarmplot(data=dfAll, x=x, y=y,order=order,hue = hue)
        elif(plotType=='strip'):
            ax = sns.stripplot(data=dfAll, x=x, y=y,order=order,hue = hue)
        elif(plotType=='violin'):
            ax = sns.violinplot(data=dfAll, x=x, y=y,order=order,hue = hue)
    
    
    #dfAll.boxplot(column='Fitness',by=['Length','Base'],ax=ax1,grid=False,notch=False)
    if(tp=='evol'):
            ax.set_ylim(-0.1,11)
    

#mainFolder: main folder containing experiment folders
#folder: array of folder headers
#tp: the type of graph 'evol','nModules','brokenConn'
#rep: number of repetitions
#indiv: boolean plot individual graphs or all in the same
#nEval: number of evaluations
def plotInertiaGraphs(mainFolder,folders,tp,rep,indiv,nEval):
    logColX = 13
    logColY = 14
    logColZ = 15
    file ='bestFeatures'
    
    
    if(not indiv):
        fig = plt.figure(figsize=(15,10))
        ax1 = fig.gca()
        
    for k in range(0,len(folders)):
        if(indiv):
            fig = plt.figure()
            ax1 = fig.gca()
        dfX = pd.DataFrame(columns=range(0,nEval))
        dfY = pd.DataFrame(columns=range(0,nEval))
        dfZ = pd.DataFrame(columns=range(0,nEval))
        
        evolBestX = []
        evolBestY = []
        evolBestZ = []
        
        for i in range(0,rep):
            evolBestX.clear()
            evolBestY.clear()
            evolBestZ.clear()
            csv_file = open('./'+mainFolder+'/'+folders[k]+'xL/'+str(i+1)+'/log/'+file+'.txt')
            #csv_file = open('./filesFromLenghtExperiment/'+folders[k]+'xL/'+str(i+1)+'/log/bestFeatures.txt')
            #csv_file = open('/content/drive/My Drive/2019/Papers/Base Length/filesFromLenghtExperiment/'+folders[k]+'xL/'+str(i+1)+'/log/evolution.txt')
            csv_reader = csv.reader(csv_file,delimiter='-')
            rows = list(csv_reader)
            evaluationsPerGen = math.floor(nEval/len(rows))
            line_count = 0
            for row in rows:
            	valueX = float(row[logColX])
            	valueY = float(row[logColY])
            	valueZ = float(row[logColZ])
            	for l in range(0,evaluationsPerGen):
                	evolBestX.append(valueX)
                	evolBestY.append(valueY)
                	evolBestZ.append(valueZ)
            if(len(evolBestX)<nEval):
            	diff = nEval - len(evolBestX)
            	for l in range(0,diff):
            		evolBestX.append(valueX)
            		evolBestY.append(valueY)
            		evolBestZ.append(valueZ)
            dfX.loc[i] = evolBestX[:]
            dfY.loc[i] = evolBestY[:]
            dfZ.loc[i] = evolBestZ[:]

        #ax1.plot(df.min(),label='Best')
        #ax1.plot(df.max(),label='Worst')
        x = range(nEval)
        q3X = dfX.quantile(0.75)
        q1X = dfX.quantile(0.25)

        q3Y = dfY.quantile(0.75)
        q1Y = dfY.quantile(0.25)

        q3Z = dfZ.quantile(0.75)
        q1Z = dfZ.quantile(0.25)

        ax1.plot(x,dfX.median(),label='MedianX'+folders[k])
        ax1.plot(x,dfY.median(),label='MedianY'+folders[k])
        ax1.plot(x,dfZ.median(),label='MedianZ'+folders[k])
        # if(indiv):
        #     ax1.plot(x,q3X, color='k', linestyle='--',label='IQR')
        #     ax1.plot(x,q3Y, color='k', linestyle='--',label='_nolegend_')
        #     ax1.plot(x,q3Z, color='k', linestyle='--',label='_nolegend_')
        # else:
        #     ax1.plot(x,q3X, color='k', linestyle='--',label='_nolegend_')
        #     ax1.plot(x,q3Y, color='k', linestyle='--',label='_nolegend_')
        #     ax1.plot(x,q3Z, color='k', linestyle='--',label='_nolegend_')
        # ax1.plot(x,q1X, color='k', linestyle='--',label='_nolegend_')
        # ax1.plot(x,q1Y, color='k', linestyle='--',label='_nolegend_')
        # ax1.plot(x,q1Z, color='k', linestyle='--',label='_nolegend_')
        # ax1.fill_between(x, q1X, q3X, alpha=0.5)
        # ax1.fill_between(x, q1Y, q3Y, alpha=0.5)
        # ax1.fill_between(x, q1Z, q3Z, alpha=0.5)
        
        #plt.axhline(y=0.3, color='k', linestyle='-.')
        if(tp=='evol'):
            ax1.set_ylim(-0.1,1.5)
        elif(tp=='nModules'):
            ax1.set_ylim(-0.1,20)
        elif(tp=='brokenConn'):
            ax1.set_ylim(-0.1,4)
        ax1.legend()
        ax1.set_title('Length x'+folders[k])
        #ax1.set_xticks([0,100,200,300])
        #ax1.set_xticklabels(['0','3000','6000','9000'])
        ax1.set_xlabel('Fitness Evaluations')
        ax1.set_ylabel('Fitness')
        #plt.savefig('CPGGenDEOne.eps',bbox_inches="tight")
    plt.show()