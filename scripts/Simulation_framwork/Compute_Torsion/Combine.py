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

ny = 100

for i in range(ny):
	filename = 'Torsions/Feature'+str(i+1)+'.txt'
	data_temp = np.loadtxt(filename) # there are 1,000,000 frames
	data_temp = np.float32(data_temp)	# change to float32, and transfer to tensor
	if(i == 0):
		data = data_temp
	else:
		data = np.concatenate((data,data_temp),axis = 0)
	print('input Feature:', i)


mask1 = np.isfinite(data[:,10])
mask2 = np.isfinite(data[:,11])
mask = mask1*mask2

Feature = data[mask,:]

N = len(Feature)

H, xgrid, ygrid = np.histogram2d(Feature[:,10],Feature[:,11],bins = 100)

H = H.transpose()


fig = plt.figure(figsize=(8,6))
ax = fig.gca()
surf = plt.imshow(-np.log(H), cmap = cm.jet, interpolation='nearest', origin='low', extent=[xgrid[0], xgrid[-1], ygrid[0], ygrid[-1]])
ax.set_xlabel(r'$\phi$',fontsize=20)
ax.set_ylabel(r'$\psi$',fontsize=20)
plt.xlim((-3.14,3.14))
plt.ylim((-3.14,3.14))
fig.colorbar(surf, shrink=1.0, aspect=9)
plt.clim(-8.2,0)
plt.savefig('FES_simulation.pdf',dpi=100)


names = ['a1','a2','a3','a4','a5','b1','b2','b3','b4','b5']

import os
import shutil

if not os.path.exists('BondAngle'):
    os.makedirs('BondAngle')
else:
	shutil.rmtree('BondAngle') 
	os.makedirs('BondAngle')

for i in range(10):

	Min = min(Feature[:,i])
	Max = max(Feature[:,i])

	step = 0.01

	grid = np.arange(Min,Max,step)

	count, bins = np.histogram(Feature[:,i], grid)

	prob_density = np.float32(count)/N/step

	#print(prob_density)


	N1 = len(bins)-1

	filename = 'BondAngle/' + names[i]+'.txt'

	x = np.concatenate((bins[:-1].reshape((N1,1)), prob_density.reshape((N1,1))),axis = 1)
	np.savetxt(filename, x, fmt='%.6f')



	AA = np.loadtxt('/scratch/jw108/Dialanine_data/6_atom/BondAngle/'+names[i]+'.txt')

	fig = plt.figure(figsize=(8, 6))
	ax = fig.gca()
	# mask = AA_b1[:,1]!=0
	plt.plot(AA[:,0],AA[:,1], c = 'blue', label = 'True distribution')
	# mask = NN_reg_b1[:,1]!=0
	plt.plot(x[:,0],x[:,1], c = 'red', label = 'Simulation')
	# mask = NN_noreg_b1[:,1]!=0
	#plt.plot(NN_noreg_b1[:,0],NN_noreg_b1[:,1], c = 'cyan', label = 'CGNet_noreg')
	# mask = NN_noreg_b1[:,1]!=0
	#plt.plot(Spline_b1[:,0],Spline_b1[:,1], c = 'green', label = 'Spline')

	ax.set_xlabel('dist',fontsize=30)
	ax.set_ylabel(r'$\rho(x)$',fontsize=30)

	plt.xticks(fontsize = 20)
	plt.yticks(fontsize = 20)

	plt.legend(loc = 'upper left')
	#plt.title(TitleAngle[i])

	#plt.show()

	filename = 'BondAngle/'+names[i]+'.pdf'
	plt.savefig(filename,dpi=300)

