# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 22:01:46 2015

@author: tong
"""

from pylab import *
import matplotlib as mpl
import random
import time
from scipy import optimize
import matplotlib.colors


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
    '''
    check if there exist span cluster , return the span cluster tuple and the ans value
    when there exist span cluster ans=0, when there exist no span cluster ans=1
    '''
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
    '''
    combination of clusters when they are juncked,
    '''
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
    '''
    one step of calculation, return the fraction number, the span clusters and all clusters
    if F=0, there are no span cluster existed
    '''
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
    '''
    for a sequence value of p, doing a series calculation of 50 times, return the effective average number of F.
    '''
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
 

'''   
#show the one configuration of cluster 
F,span,xcluster,ycluster,grid=solution(100,0.59)
l=len(xcluster)
cl=np.linspace(0,1,l)
figure(figsize=(10,10))
for i in range(len(xcluster)):
    if (len(xcluster[i])!=0):
        plot(xcluster[i],ycluster[i],'o')
savefig('show0.59-2.png',dpi=800)

'''    
    
'''
p=linspace(0.60,0.90,30)
F,a=final(100,p)
print p
print F
plt.plot(p,F)
'''

'''
# results of solution of 100 grids. 
p=array([0.6 , 0.61034483 , 0.62068966 , 0.63103448 , 0.64137931 , 0.65172414,
  0.66206897 , 0.67241379 , 0.68275862 , 0.69310345 , 0.70344828 , 0.7137931,
  0.72413793 , 0.73448276 , 0.74482759 , 0.75517241 , 0.76551724 , 0.77586207,
  0.7862069  , 0.79655172 , 0.80689655 , 0.81724138 , 0.82758621 , 0.83793103,
  0.84827586 , 0.85862069 , 0.86896552 , 0.87931034 , 0.88965517 , 0.9       ]

)
F=array([0.56404391 , 0.69646764 , 0.79843208 , 0.86442536 , 0.90419613 , 0.9200564,
  0.94378756 , 0.95536067 , 0.96459492 , 0.97172341 , 0.97645554 , 0.98123457,
  0.98592279 , 0.98822664 , 0.99041563 , 0.99276496 , 0.99380738 , 0.99509342,
  0.9960971  , 0.99696807 , 0.9974838  , 0.9982    , 0.9985756  , 0.99882591,
  0.99912255 , 0.99942017 , 0.99947953 , 0.9996425 ,  0.99975722 , 0.99984228]

) 

plt.xlabel("$Occupation\  Probability \ p$",fontsize=16)
plt.ylabel("$Fraction \ F$", fontsize=16)
plt.plot(p,F,'r')
plt.savefig('P1.png',dpi=800)    

'''


'''
#fit solution of problem b)
p=array([0.6 , 0.61034483 , 0.62068966 , 0.63103448 , 0.64137931 , 0.65172414])
F=array([0.56404391 , 0.69646764 , 0.79843208 , 0.86442536 , 0.90419613 , 0.9200564])
l=len(p)
plog=zeros(l)
Flog=zeros(l)
Ffit=zeros(l)
for i in range(l):
    plog[i]=log(p[i])
    Flog[i]=log(F[i])
    

def fit(x,a,b,c):
    return a+b*log(x-c)

guess=array([0.8,0.6,0.4])
a,b=optimize.curve_fit(fit,p,Flog,guess)
print a
for i in range(l):
    Ffit[i]=fit(p[i],a[0],a[1],a[2])
print Ffit
toWrite= "fit curve: ln(F) = %f + %f*ln(p-%f)" % (a[0],a[1],a[2])
plt.xlabel("$Occupation\  Probability \ p$",fontsize=16)
plt.ylabel("$Fraction \ ln(F)$", fontsize=16)
plt.plot(p,Ffit,'r',label="$Curve \ fit$")
plt.plot(p,Flog,'b',label="$Calculation \ Result$")
plt.text(0.61,-0.4,toWrite)
plt.legend(loc='best',fontsize=14)
plt.savefig('P2.png',dpi=800)
'''
#plt.plot(p,Ffit,'b')
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