# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 22:01:46 2015

@author: tong
"""

from pylab import *
import matplotlib as mpl
import random
import time




def initialize(n):
	'''
	initialize n*n grids and the vacant position 
	'''
	grid = zeros((n,n))
	vacancy = []
	for i in range(n):
		for j in range(n):
			vacancy.append([i,j])
	return grid, vacancy 

def selection(vacancy,grid):	
    choice = random.choice(vacancy)
    p0=int(choice[0])
    p1=int(choice[1])
    vacancy.remove([p0,p1])
    return choice 

def gainxy(x,y,xcluster,ycluster):
	'''
	subtract x y from the random choice,and add it to the list
	'''
	xcluster=xcluster+([x],)
	ycluster=ycluster+([y],)

	return xcluster, ycluster


def listcomb(num1, num2, xcluster,ycluster):
	'''
	add the elements in cluster#num2 to cluster#num1 when num1<num2
	'''		
	l = len(xcluster[num2])
	for i in range(l):
		xcluster[num1].append(xcluster[num2][l-1-i])
		ycluster[num1].append(ycluster[num2][l-1-i])
		xcluster[num2].pop()
		ycluster[num2].pop()	
	return

def renumgrid(num1,num2,xcluster,ycluster,grid):
	'''
	renumber the number elements in grid when cluster2 join to
	'''
	l = len(xcluster[num2]) 
	for i in range(l):
		x=int(xcluster[num2][i])
		y=int(ycluster[num2][i])
		grid[x][y]=num1
	return

def percolation(num1,num2,xcluster,ycluster,grid):
	if (num1<num2):
		renumgrid(num1,num2,xcluster,ycluster,grid)
		listcomb(num1, num2, xcluster, ycluster)
	if (num1>num2):
		renumgrid(num2,num1,xcluster,ycluster,grid)
		listcomb(num2, num1, xcluster, ycluster)
	return

def check(xcluster,ycluster,n):
    ans = 1
    span = []
    for i in range(len(xcluster)):
        if (len(xcluster[i])!=0):
            if(min(xcluster[i])==0 and max(xcluster[i])==n-1):	
                num  = i
                ans = 0
                span.append([i,len(xcluster[i])])
            elif(min(ycluster[i])==0 and max(ycluster[i])==n-1):
                num = i
                ans = 0
                span.append([i,len(xcluster[i])])
    return ans, span

def combine(x,y,n,xcluster,ycluster,grid):
    if x<n-1:
        if (grid[x+1][y]):
            num1=int(grid[x+1][y])
            num2=int(grid[x][y])
            percolation(num1,num2,xcluster,ycluster,grid)
    if x>0:
        if (grid[x-1][y]):
            num1=int(grid[x-1][y])
            num2=int(grid[x][y])
            percolation(num1,num2,xcluster,ycluster,grid)
    if y<n-1:
        if (grid[x][y+1]):
            num1=int(grid[x][y+1])
            num2=int(grid[x][y])
            percolation(num1,num2,xcluster,ycluster,grid)
    if y>0:
        if (grid[x][y-1]):
            num1=int(grid[x][y-1])
            num2=int(grid[x][y])
            percolation(num1,num2,xcluster,ycluster,grid)
    return
             


def solution(n,p):
    grid,vacancy = initialize(n)
    ans=1
    clnum=1
    xcluster=([],)
    ycluster=([],)
    total=0
    nc=0
    while(len(vacancy)!=0):
        select = selection(vacancy,grid)
        x =int(select[0])
        y=int(select[1])
        c=random.random()
        if c < p:
            grid[x][y] = clnum
            xcluster,ycluster=gainxy(x,y,xcluster,ycluster)
            combine(x,y,n,xcluster,ycluster,grid)
            clnum += 1
    ans,span = check(xcluster,ycluster,n)
    for i in range(len(xcluster)):
        if (len(xcluster[i])!=0):
            total += len(xcluster[i])
    for i in range(len(span)):
        if (len(span[i])!=0):
            nc += span[i][1] 
    F=float(nc)/float(total)               
    return F,span,xcluster,ycluster,grid


def final(n,p):
    l=len(p)
    total=zeros((l,50))
    F=zeros(l)
    a=0
    for i in range(l):
        for j in range(50):
            total[i][j],span,xcluster,ycluster,grid = solution(n,p[i])
            if (total[i][j]!=0):
                F[i]=F[i]+total[i][j]
                a=a+1
        F[i]=float(F[i])/float(a)
        print a
        a=0
    return F,a

p=linspace(0.60,0.70,5)
F,a=final(50,p)
print p
print F
plt.plot(p,F)
'''
p=array([ 0.65 ,       0.65689655 , 0.6637931   ,0.67068966 , 0.67758621,  0.68448276,
  0.69137931 , 0.69827586 , 0.70517241 , 0.71206897 , 0.71896552 , 0.72586207,
  0.73275862 , 0.73965517 , 0.74655172 , 0.75344828 , 0.76034483 , 0.76724138 ,
  0.77413793 , 0.78103448 , 0.78793103 , 0.79482759 , 0.80172414 , 0.80862069,
  0.81551724 , 0.82241379 , 0.82931034 , 0.8362069  , 0.84310345 , 0.85      ]
)
F=array([ 0.35937038 , 0.38004543 , 0.44000397 , 0.4115973 ,  0.39243808 , 0.36536844,
  0.44173034 , 0.37792407 , 0.39071663 , 0.3970174  , 0.41946921 , 0.38999831,
  0.42840531 , 0.40828894 , 0.41540073 , 0.39130996 , 0.39255681 , 0.39857331,
  0.41476819 , 0.42124591 , 0.39507906 , 0.38222086 , 0.41098439 , 0.40689961,
  0.39580929 , 0.41692609 , 0.42680671 , 0.409812 ,   0.42114223 , 0.42629931]
)       

l=len(p)
plog=zeros(l)
Flog=zeros(l)
for i in range(l):
    plog[i]=log(p[i]-0.62)
    Flog[i]=log(F[i])
plt.plot(plog,Flog)    
'''
#F,span,xcluster,ycluster,grid = solution(5,0.6)
#print F
#print span
#print xcluster
#print ycluster
#print nc
#print num
#figure(figsize=(10,10))
#xlim(-0.5,9.5)
#ylim(-0.5,9.5)
#plot(xcluster[num],ycluster[num],'bo',markersize=50)