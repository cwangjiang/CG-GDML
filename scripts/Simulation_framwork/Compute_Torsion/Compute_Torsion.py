# This code compute dihedral of the trajectory and compute density distribution.

# import torch
# import torch.nn as nn
# import torch.nn.functional as F 
# import torch.optim as optim
# from torchvision import datasets, transforms
import numpy as np 

import matplotlib.pyplot as plt 
import matplotlib
plt.switch_backend('agg')
from matplotlib import cm

#from torch.utils.data import Dataset, DataLoader
import math

ID =

# ny = 100

# for i in range(ny):
# 	filename = 'TRAJs/Simtraj_'+str(i+1)+'.txt'
# 	data_temp = np.loadtxt(filename) # there are 1,000,000 frames
# 	data_temp = np.float32(data_temp)	# change to float32, and transfer to tensor
# 	if(i == 0):
# 		data = data_temp
# 	else:
# 		data = np.concatenate((data,data_temp),axis = 0)
# 	print('input Simtraj:', i)


filename = '../../TRAJs/Simtraj_'+str(ID)+'.txt'
data = np.loadtxt(filename) # there are 1,000,000 frames
data = np.float32(data)	# change to float32, and transfer to tensor
# if(i == 0):
# 	data = data_temp
# else:
# 	data = np.concatenate((data,data_temp),axis = 0)
# print('input Simtraj:', i)




# data = data_temp[:,0:18]

N = len(data)



def Compute_feature(data):

	Feature = np.zeros((N,12)) # a1,a2,a3,b1,b2,b3,b4,phi,psi

	for i in range(len(data)):
		p1 = data[i,0:3] # five atom coordinats
		p2 = data[i,3:6]
		p3 = data[i,6:9]
		p4 = data[i,9:12]
		p5 = data[i,12:15]
		p6 = data[i,15:18]

		v1 = p2 - p1  # for vectors
		v2 = p3 - p2
		v3 = p5 - p3
		v4 = p6 - p5
		v5 = p4 - p3

		c1 = np.cross(v1,v2) # three normal vectors
		c2 = np.cross(v2,v3)
		c3 = np.cross(v3,v4)

		dot1 = np.dot(c1,c2)/np.linalg.norm(c1)/np.linalg.norm(c2) # two dot products
		dot2 = np.dot(c2,c3)/np.linalg.norm(c2)/np.linalg.norm(c3)

		if(dot1>1.0): # in case some dot is slightly larger than 1.0 due to rounding error
			dot1 = 1.0
		if(dot1<-1.0):
			dot1 = -1.0

		if(dot2>1.0):
			dot2 = 1.0
		if(dot2<-1.0):
			dot2 = -1.0	

		phi = math.acos(dot1) # compute angle [0, 180]
		psi = math.acos(dot2)

		phi = phi*np.sign(np.dot(v1,c2)) # extend angle to [-180,180], since the backbone has direction
		psi = psi*np.sign(np.dot(v4,c2))

		b1 = np.linalg.norm(v1)
		b2 = np.linalg.norm(v2)
		b3 = np.linalg.norm(v3)
		b4 = np.linalg.norm(v4)
		b5 = np.linalg.norm(v5)

		a1 = math.acos(np.dot(v1,v2)/b1/b2)
		a2 = math.acos(np.dot(v2,v3)/b2/b3)
		a3 = math.acos(np.dot(v3,v4)/b3/b4)
		a4 = math.acos(np.dot(v2,v5)/b2/b5)
		a5 = math.acos(-np.dot(v5,v3)/b3/b5)

		Feature[i,:] = [a1,a2,a3,a4,a5,b1,b2,b3,b4,b5,phi,psi]

		if(i%10000 == 0):
			print('i = ',i)

	return Feature

Feature = Compute_feature(data)

filename = '../Torsions/Feature'+str(ID)+'.txt'

np.savetxt(filename, Feature, fmt='%.6f')


exit()
