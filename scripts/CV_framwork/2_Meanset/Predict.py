import numpy as np
from sgdml.predict import GDMLPredict
from sgdml.utils import io
import time
import os
import shutil

data = np.loadtxt('/scratch/jw108/Dialanine_data/6_atom/.txt')

N = 3000
Nm = 1000 # number of models

Config = data[0:N,0:18]
Force = np.zeros((N,18))

for i in np.arange():
	modelname = '../../1_LV1Training/NPZs/batch'+str(i+1)+'-unknown-train999-sym1.npz'
	model = np.load(modelname)
	gdml = GDMLPredict(model)
	print('i=',i)
	e,f = gdml.predict(Config)
	Force = Force + f

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

#Meanset = np.concatenate((Config,Force),axis = 1)

filename = '../AccumulateForce/AccumulateForce'+str()+'.txt'

np.savetxt(filename, Force, fmt='%.6f')



exit()
