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


Torsion = np.loadtxt('../../5_atom/Torsion.txt')
coordforce = np.load('../dialanine_6atom/coordforce_6atom.npy') # there are 1,000,000 frames

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
		
	# if(Torsion[i,0]<(0+Max) or (Torsion[i,0]>(2+Max))):
	# 	continue
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
		sample_bin_index = np.random.choice(O, L, replace=False)
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

L = 3000 # each batch contain L uniform points
T = 1 # sample T batches.

for i in range(T):
	filename = 'coordforce_6atom_Uniform_3k.txt'
	Point_index = Unifsample(L,filename)

	if(i%10 == 0):
		print('i =', i)

	fig = plt.figure(figsize=(8, 6))
	ax = fig.gca()
	surf = plt.scatter(Torsion[Point_index,0],Torsion[Point_index,1], c = 'blue', marker='.',s=1)
	ax.set_xlabel(r'$\phi$',fontsize=20)
	ax.set_ylabel(r'$\psi$',fontsize=20)
	plt.xlim((-Max,Max))
	plt.ylim((-Max,Max))
	plt.title('Torsion')
	plt.savefig('Torsion_Uniform_3k.png',dpi=300)

exit()







