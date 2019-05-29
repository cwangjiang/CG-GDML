import numpy as np
from sgdml.predict import GDMLPredict
from sgdml.utils import io
import time
import os
import shutil


CVErs = np.zeros((1,5))

for i in range(5): # 5 folds
	CVEr = 0
	for j in range(10): # 10 parallel sections
		filename = 'SqErs/SqEr'+str(i+1)+'_'+str(j+1)+'.txt'
		temp = np.loadtxt(filename)
		CVEr = CVEr + temp.item()
	CVErs[0,i] = CVEr/20/10

mean = np.mean(CVErs)
error = np.std(CVErs)/np.sqrt(5)

filename = 'CV.txt'
f = open(filename,'w')
# print(SqEr, file = f)
print >>f, 'CV = ', mean, '+/-', error
f.close()

exit()
