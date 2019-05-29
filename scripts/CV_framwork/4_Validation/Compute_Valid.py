import numpy as np
from sgdml.predict import GDMLPredict
from sgdml.utils import io
import time
import os
import shutil

foldID =
parallelID =

modelname = '../../3_LV2Training/Meanset'+str(foldID)+'-unknown-train2999-sym1.npz'
model = np.load(modelname)
gdml = GDMLPredict(model)

SqEr = 0.0

start = 1000-foldID*200 + parallelID*20-20
end = start + 20

for i in np.arange(start, end):
	data = np.load('/scratch/jw108/Dialanine_data/6_atom//batch'+str(i+1)+'.npz')
	Config = data['R'].reshape(1000,18)
	Instforce = data['F'].reshape(1000,18)
	e, Predictforce = gdml.predict(Config)
	SqEr = SqEr + np.sum((Instforce - Predictforce)**2)/1000/18

filename = '../SqErs/SqEr'+str(foldID)+'_'+str(parallelID)+'.txt'
# f = open(filename,'w')
# print(SqEr, file = f)
# f.close()

import sys
sys.stdout = open(filename,'wt')
print(SqEr)

exit()
