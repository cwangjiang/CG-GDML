import numpy as np
from sgdml.predict import GDMLPredict
from sgdml.utils import io
import time
import os
import shutil

# r,_ = io.read_xyz('/home/jw108/Remount/GDML/abc.xyz') # 9 atoms
# print r.shape # (1,27)

model = np.load('../Meanset1-unknown-train2999-sym1.npz')

BondConst = np.loadtxt('../BondConst.txt') 
BondConst = np.float32(BondConst)

gdml = GDMLPredict(model)
# e,f = gdml.predict(r)
# print e.shape # (1,)
# print f.shape # (1,27)


rr = np.random.randn(1,18)
e,f = gdml.predict(rr)
print e.shape
print f.shape
print(e,f)


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

	return F.reshape(1,18)



beta = 1.6775
#Distance_edge = np.loadtxt('Distance_edge_6atom.txt') 

def Simulate(x0, dt, T, freq):

	X = np.zeros((int(T/freq), ny, 18))
    # f = np.zeros((T, 2))
	X[0,:,:] = x0
	x_old = x0
	t1 = time.time()

	for t in range(1, T):
		if(t%1000 == 0):
			print('t = ', t)
			t2 = time.time()
			DT = t2 - t1
			remain_ts = int((T-t)/1000*DT)
			remain_m = int(remain_ts/60)
			remain_s = remain_ts - remain_m*60
			print 'remain time:'+str(remain_m)+'min '+str(remain_s)+'s'
			t1 = time.time()


		e, force = gdml.predict(x_old)

		force = force + Compute_PriorF(x_old)

		x_new = x_old + force*dt + np.sqrt(2*dt/beta)*np.random.randn(ny,18)

		if(np.sum(np.isnan(x_new[0]))):
			print(x_new)
			
		#print(x_new)

		if(t%freq == 0):
			X[int(t/freq),:] = x_new

		x_old = x_new
		x_old = np.float32(x_old)
	return X

#x0 = np.array([-78.433485, 27.714482, 36.402416, -78.059635, 29.002239, 36.159638, -77.824640, 29.923691, 37.226781, -78.832874, 31.032275, 37.308817, -79.831244, 31.125854, 36.412319])
#x0 = np.array([212.808840, 232.405540, -68.260515, 211.822750, 231.500130, -68.331115, 211.277985, 230.840341, -67.130350, 210.594954, 231.760225, -66.146997, 209.985973, 232.859419, -66.665403])


ny = 1


data = np.loadtxt('/home/jw108/Remount_Davinci/Dialanine_data/6atoms/coordforce_6atom_3k.txt')
data = np.float32(data)
# np.random.seed(5)
sample = np.random.choice(3000,ny, replace = False)
# x0 = data[sample,np.array([0,1,2,3,4,5,6,7,8,12,13,14,15,16,17])]
x0 = data[sample,0:18]

freq = 200
T = 10000000
T = 2000000
dt = 2e-4

Simtraj = Simulate(x0, dt, T, freq)
Simtraj = np.float32(Simtraj)
#Simtraj3 = np.float32(Simtraj3)

ID = 

filename = '../TRAJs/Simtraj_'+str(ID)+'.txt'

np.savetxt(filename, Simtraj[:,0,:].reshape(-1,18), fmt='%.4f')


exit()

# modelID = 17

# pathname = '/home/jw108/Remount/GDML/Simulation_results/model' + str(modelID) + '/Simtraj'

# if not os.path.exists(pathname):
#     os.makedirs(pathname)
# else:
# 	shutil.rmtree(pathname) 
# 	os.makedirs(pathname)


# for i in range(ny):
# 	filename = pathname + '/Simtraj_' + str(i+1)+'.txt'
# 	np.savetxt(filename, Simtraj[:,i,:], fmt='%.6f')
