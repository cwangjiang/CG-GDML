# This code uniform sample 4579 point from coordforce_6atom.txt

import torch
import torch.nn as nn
import torch.nn.functional as F 
import torch.optim as optim
from torchvision import datasets, transforms
import numpy as np 

import matplotlib.pyplot as plt 
import matplotlib
plt.switch_backend('agg')
from matplotlib import cm

from torch.utils.data import Dataset, DataLoader
import math

import os
import shutil
if not os.path.exists('TXT'):
    os.makedirs('TXT')
else:
	shutil.rmtree('TXT') # remove everything in the folder, I don't have to use this.
	os.makedirs('TXT')


Torsion = np.loadtxt('../../5_atom/Torsion.txt')
coordforce = np.load('../dialanine_6atom/coordforce_6atom.npy') # there are 1,000,000 frames

BondConst = np.loadtxt('BondConst.txt') 
BondConst = np.float32(BondConst)

def bondforce(V,NORM,b0,kb):
	F =  kb*(NORM-b0)*V/NORM
	return F

def angleforce(V1,V2,NORM1,NORM2,ANGLE,a0,COS,ka):
 
	F1 = -ka*(ANGLE-a0)*1/np.sqrt(1-COS**2)*1/NORM1*(-V1/NORM1*COS+V2/NORM2)
	F3 = ka*(ANGLE-a0)*1/np.sqrt(1-COS**2)*1/NORM2*(-V2/NORM2*COS+V1/NORM1)
	F2 = -F1-F3
	return F1, F2, F3

def Compute_PriorF(coord): 

	coord = coord[:,0:18]
	n = len(coord)
	v = np.zeros((5,n,3))
	NORM = np.zeros((5,n,1))
	COS = np.zeros((5,n,1))
	ANGLE = np.zeros((5,n,1))


	v[0,:,:] = coord[:,3:6] - coord[:,0:3]
	v[1,:,:] = coord[:,6:9] - coord[:,3:6]
	v[2,:,:] = coord[:,12:15] - coord[:,6:9]	
	v[3,:,:] = coord[:,15:18] - coord[:,12:15]
	v[4,:,:] = coord[:,9:12] - coord[:,6:9]

	NORM[0,:,:] = np.linalg.norm(v[0,:,:],axis = 1,keepdims=True)
	NORM[1,:,:] = np.linalg.norm(v[1,:,:],axis = 1,keepdims=True)
	NORM[2,:,:] = np.linalg.norm(v[2,:,:],axis = 1,keepdims=True)
	NORM[3,:,:] = np.linalg.norm(v[3,:,:],axis = 1,keepdims=True)
	NORM[4,:,:] = np.linalg.norm(v[4,:,:],axis = 1,keepdims=True)

	COS[0,:,:] = np.sum(v[0,:,:]*v[1,:,:],axis = 1, keepdims=True)/NORM[0,:,:]/NORM[1,:,:]
	COS[1,:,:] = np.sum(v[1,:,:]*v[2,:,:],axis = 1, keepdims=True)/NORM[1,:,:]/NORM[2,:,:]
	COS[2,:,:] = np.sum(v[2,:,:]*v[3,:,:],axis = 1, keepdims=True)/NORM[2,:,:]/NORM[3,:,:]
	COS[3,:,:] = np.sum(v[1,:,:]*v[4,:,:],axis = 1, keepdims=True)/NORM[1,:,:]/NORM[4,:,:]
	COS[4,:,:] = np.sum(-v[4,:,:]*v[2,:,:],axis = 1, keepdims=True)/NORM[2,:,:]/NORM[4,:,:]

	ANGLE[0,:,:] = np.arccos(COS[0,:,:])
	ANGLE[1,:,:] = np.arccos(COS[1,:,:])
	ANGLE[2,:,:] = np.arccos(COS[2,:,:])
	ANGLE[3,:,:] = np.arccos(COS[3,:,:])
	ANGLE[4,:,:] = np.arccos(COS[4,:,:])

	F = np.zeros((6,n,3))

	# bond forces
	bondatomIndex = np.array([[0,1],[1,2],[2,4],[4,5],[2,3]]) # 2 atoms associated with each bond
	for i in range(5): # five bonds
		F_temp = bondforce(v[i,:,:],NORM[i,:,:],BondConst[i,0],BondConst[i,1])
		F[bondatomIndex[i,0],:,:] = F[bondatomIndex[i,0],:,:] + F_temp
		F[bondatomIndex[i,1],:,:] = F[bondatomIndex[i,1],:,:] - F_temp

	angleatomIndex = np.array([[0,1,2],[1,2,4],[2,4,5],[1,2,3],[3,2,4]]) # 2 atoms associated with each bond
	anglebondIndex = np.array([[0,1],[1,2],[2,3],[1,4],[4,2]])
	# angle forces
	for i in range(5): # five angle
		if(i==4):
			F1,F2,F3 = angleforce(-v[anglebondIndex[i,0],:,:],v[anglebondIndex[i,1],:,:],NORM[anglebondIndex[i,0],:,:],NORM[anglebondIndex[i,1],:,:],ANGLE[i,:,:],BondConst[i+5,0],COS[i,:,:],BondConst[i+5,1])
		else:
			F1,F2,F3 = angleforce(v[anglebondIndex[i,0],:,:],v[anglebondIndex[i,1],:,:],NORM[anglebondIndex[i,0],:,:],NORM[anglebondIndex[i,1],:,:],ANGLE[i,:,:],BondConst[i+5,0],COS[i,:,:],BondConst[i+5,1])
		F[angleatomIndex[i,0],:,:] = F[angleatomIndex[i,0],:,:] + F1
		F[angleatomIndex[i,1],:,:] = F[angleatomIndex[i,1],:,:] + F2
		F[angleatomIndex[i,2],:,:] = F[angleatomIndex[i,2],:,:] + F3

	return F


PriorF = Compute_PriorF(coordforce[:,0:18])
print(PriorF[:,0,:])
PriorF_new = np.zeros((1000000,18))
for i in range(1000000):
	PriorF_new[i,:] = PriorF[:,i,:].reshape(1,18)
print(PriorF_new[0,:])

# print(coordforce[0,:])
coordforce[:,18:36] = coordforce[:,18:36] - PriorF_new
# print(coordforce[0,:])

# exit()

N = len(Torsion)

# loop over all N point, create Space index board, and index dictionary

print('Creating Index Board...')

Min = -3.141592653
Max = 3.141592653

Torsion = Torsion + Max

gridN = 300

Step = (2*3.141592653)/gridN

IndexBoard = np.zeros((gridN,gridN))

Mymap = {}

BinIdx = 1

for i in range(N):
	x = int(Torsion[i,0]/Step)
	y = int(Torsion[i,1]/Step)

	if(x==gridN):
		x=gridN-1
	if(y==gridN):
		y=gridN-1

	if(IndexBoard[x,y]==0):
		IndexBoard[x,y] = BinIdx
		Mymap[BinIdx] = np.array([i])		
		BinIdx = BinIdx+1
	else:
		ID = IndexBoard[x,y]
		Mymap[ID] = np.append(Mymap[ID],i)
	if(i%10000 == 0):
		print('i =', i)

Torsion = Torsion - Max
O = len(Mymap)
print(len(Mymap))

# Define an random sampling function

def Unifsample(L,filename):
	if(L<=O):
		sample_bin_index = np.random.choice(O, L, replace=True)
	else:
		sample_bin_index = np.random.choice(O, L, replace=True)

	# for each sampled bin, randomly choise one configuration

	Point_index = np.zeros((L))
	for i in range(L):
		Point_index[i] = np.random.choice(Mymap[sample_bin_index[i]+1])


	Point_index = Point_index.astype(int)	 # force change to int
	#print(Point_index[1])

	sample_subset = coordforce[Point_index,:]
	np.savetxt(filename,sample_subset,fmt='%.6f')

	return Point_index


# Execute the sampling function 1000 times, save 1000 files. 

print('Creating batches...')

L = 1000 # each batch contain L uniform points
T = 1000 # sample T batches.

for i in range(T):
	filename = 'TXT/batch'+str(i+1)+'.txt'
	Point_index = Unifsample(L,filename)

	if(i%10 == 0):
		print('i =', i)

	if(i == 500):
		fig = plt.figure(figsize=(8, 6))
		ax = fig.gca()
		surf = plt.scatter(Torsion[Point_index,0],Torsion[Point_index,1], c = 'blue', marker='.',s=1)
		ax.set_xlabel(r'$\phi$',fontsize=20)
		ax.set_ylabel(r'$\psi$',fontsize=20)
		plt.title('Torsion')
		plt.savefig('Torsion_U.png',dpi=300)

exit()







