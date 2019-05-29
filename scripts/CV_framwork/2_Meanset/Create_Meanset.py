import numpy as np
from sgdml.predict import GDMLPredict
from sgdml.utils import io
import time
import os
import shutil

data = np.loadtxt('/scratch/jw108/Dialanine_data/6_atom/.txt')

N = 3000
Nm = int(1000*0.8) # number of models for each fold

Config = data[0:N,0:18]
Force = np.zeros((N,18))

select = np.zeros((5,40)) # each folds contain only 40 accumulate force, which is 80 batches.

select[0,:] = np.arange(0,40)
select[1,:] = np.concatenate((np.arange(0,30),np.arange(40,50)))
select[2,:] = np.concatenate((np.arange(0,20),np.arange(30,50)))
select[3,:] = np.concatenate((np.arange(0,10),np.arange(20,50)))
select[4,:] = np.arange(10,50)


for i in range(5): # five folds
	Force = np.zeros((N,18))

	for j in select[i,:]: # 50 forcese, 1000 batches. 
		forcename = 'AccumulateForce/AccumulateForce'+str(int(j+1))+'.txt'
		f = np.loadtxt(forcename)
		Force = Force + f

	Force = Force/Nm

	Meanset = np.concatenate((Config,Force),axis = 1)

	filename = 'Meanset'+str(i+1)+'.txt'

	np.savetxt(filename, Meanset, fmt='%.6f')

# for i in range(Nm):
# 	modelname = '/scratch/jw108/model19/NPZs/batch'+str(i+1)+'-unknown-train999-sym1.npz'
# 	model = np.load(modelname)
# 	gdml = GDMLPredict(model)
# 	for j in range(N):
# 		if(j%1000==0):
# 			print('i=',i,'j=',j)
# 		e,f = gdml.predict(Config[j,:])
# 		Force[j,:] = Force[j,:] + f

#Force = Force/Nm

#print(Config.shape, Force.shape)

# Meanset = np.concatenate((Config,Force),axis = 1)

# filename = 'Meanset.txt'

# np.savetxt(filename, Meanset, fmt='%.6f')


exit()
