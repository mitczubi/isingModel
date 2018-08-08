from __future__ import division
import numpy as np 
from numpy.random import rand
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys
class Ising():
	def mcmove(self, config, N, beta):
		for i in range(N):
			for j in range(N):
				a = np.random.randint(0, N)
				b = np.random.randint(0, N)
				s = config[a,b]
				nb = config[(a+1)%N,b] + config[a,(b+1)%N] + config[(a-1)%N,b] + config[a,(b-1)%N]
				cost = 2*s*nb
				if cost < 0:
					s *= -1
				elif rand() < np.exp(-cost*beta):
					s *= -1
				config[a,b] = s
		return config
	
	def simulate(self):

		N,temp = 64, 8.4
		config = 2*np.random.randint(2,size=(N,N))-1
		f = plt.figure(figsize=(15,15), dpi=1000);
		self.configPlot(f, config, 0, N, 1);

		msrmnt = 1001
		for i in range(0,msrmnt):
			self.mcmove(config, N, 1.0/temp)
			self.configPlot(f,config,i,N,2)
			#if i == 4:
			#	self.configPlot(f,config,i,N,3)
			#if i == 32:
			#	self.configPlot(f,config,i,N,4)
			#if i == 100:
			#	self.configPlot(f,config,i,N,5)
			#if i == 1000:
			#	self.configPlot(f,config,i,N,6)

	def configPlot(self, f, config, i, N, n_):
		plt.clf()
		X, Y = np.meshgrid(range(N), range(N))
		sp = plt.subplot()
		plt.setp(sp.get_yticklabels(), visible=False)
		plt.setp(sp.get_xticklabels(), visible=False)
		plt.pcolormesh(X,Y,config,cmap=plt.cm.RdBu);
		plt.title('Time=%d'%i); plt.axis('tight')
		plt.savefig("{}.jpg".format(i))
	
rm = Ising()
rm.simulate()
#This command will replace an older version of the movie.png 
#os.system("rm movie.mp4")
#The 0.08 signifies how long each image "lives" in a video change it if you want your video to run for a longer/shorter time
os.system("ffmpeg -f image2 -r 1/0.08 -i %d.jpg -vcodec libx264 -y T8_4.mp4")
#This command will get rid of all the saved plots
os.system("rm *.jpg")


