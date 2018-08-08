#%matplotlib inline 
from __future__ import division 
import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt 

#################################################
#                Define function for ising
################################################

def initialise(N):
	# random spin state
	state = 2*np.random.randint(2, size=(N,N))-1
	return state

def mcmove(config, beta):
	for i in range(N):
		for j in range(N):
			a = np.random.randint(0, N)
			b = np.random.randint(0, N)
			s = config[a, b]
			nb = config[(a+1)%N,b] + config[a,(b+1)%N] + config[(a-1)%N,b] + config[a,(b-1)%N]
			cost = 2*s*nb
			if cost < 0:
				s *= -1
			elif rand() < np.exp(-cost*beta):
				s *= -1 
			config[a,b] = s
	return config

def calcEnergy(config):
	#give energy
	energy = 0 
	for i in range(len(config)):
		for j in range(len(config)):
			S = config[i,j]
			nb = config[(i+1)%N,j] + config[i,(j+1)%N] + config[(i-1)%N,j] + config[i,(j-1)%N]
			energy += -nb*S
	return energy/4.

def calcMag(config):
	mag = np.sum(config)
	return mag

# Main program #

nt 	= 2**8  # number of temp points
N 	= 2**4  # number of lattice point, NxN
eqSteps = 2**10 # number of MC sweeps for equilibrium
mcSteps = 2**10 # number of MC sweeps for calculation

n1, n2 = 1.0/(mcSteps*N*N), 1.0/(mcSteps*mcSteps*N*N)
tm = 2.269; T = np.random.normal(tm, .64, nt)
T = T[(T>1.2) & (T<14.0)]; nt = np.size(T)

Energy	     = np.zeros(nt); Magnetization  = np.zeros(nt)
SpecificHeat = np.zeros(nt); Susceptibility = np.zeros(nt)

# Main part of code

for m in range(len(T)):
	E1 = M1 = E2 = M2 = 0
	config = initialise(N)
	iT = 1.0/T[m]; iT2=iT*iT

	for i in range(eqSteps):
		mcmove(config, iT)

	for i in range(mcSteps):
		mcmove(config, iT)
		Ene = calcEnergy(config)
		Mag = calcMag(config)

		E1 = E1 + Ene
		M1 = M1 + Mag
		M2 = M2 + Mag*Mag
		E2 = E2 + Ene*Ene

		Energy[m] 	 = n1*E1
		Magnetization[m] = n1*M1
		SpecificHeat[m]  = (n1*E2 - n2*E1*E1)*iT2
		Susceptibility[m]= (n1*M2 - n2*M1*M1)*iT

f = plt.figure(figsize=(18,10)); 

sp = f.add_subplot(2,2,1);
plt.plot(T,Energy,'o',color="#A60628");
plt.xlabel("Temperature (T)", fontsize=20);
plt.ylabel("Energy ", fontsize=20);

sp = f.add_subplot(2,2,2);
plt.plot(T, abs(Magnetization), 'o', color="#348ABD");
plt.xlabel("Temperature (T)", fontsize=20);
plt.ylabel("Magnetization ", fontsize=20);
 			
sp = f.add_subplot(2,2,3);
plt.plot(T, SpecificHeat, 'o', color="#A60628");
plt.xlabel("Temperature (T)", fontsize=20);
plt.ylabel("Specific Heat ", fontsize=20);

sp = f.add_subplot(2,2,4);
plt.plot(T,Susceptibility, 'o', color="#348ABD");
plt.xlabel("Temperature (T)", fontsize=20);
plt.ylabel("Susceptibility ", fontsize=20);

plt.show()
