import random
import math
from trackFetcher import TrackFetcher
from spotifySongLoader import SpotifyLoader

class GeneticAlgorithm(object):
	"""docstring for GeneticAlgorithm"""
	def __init__(self, initialSize,songList,ENAPIKey):
		self.population = []
		self.songList = songList
		self.getDataForSongs(self.songList,ENAPIKey)
		self.generatePopulation(self.songList,initialSize)
		print(self.population[0])
		self.SortPopulation()
		#tests
		# print(self.population)
		# print(self.songInfo)
	
	def Merge(self,l,r,lf,rf):
		result = []
		printOut = False
		if(l == [3,7,7,26]):
			printOut = True

		while(len(l) > 0 or len(r) > 0):
			if(len(l) > 0 and len(r) > 0):
				if(lf[0] <= rf[0]):

					result.append(l.pop(0))
					lf.pop(0)
				else:
					result.append(r.pop(0))
					rf.pop(0)
			elif(len(l) > 0):
				result.extend(l)
				l = []
				lf = []
			else:
				result.extend(r)
				r = []
				rf = []
		return result

	def MergeSort(self,li,fitness):
		if(len(li) <= 1):
			return li

		mid = (len(li) + 1) / 2
		
		l = li[0:mid]


		lf = fitness[0:mid]

		l = self.MergeSort(l,lf)
		lf = self.MergeSort(lf,lf)


		r = li[mid:]

		rf = fitness[mid:]

		r = self.MergeSort(r,rf)
		rf = self.MergeSort(rf,rf)

		result = self.Merge(l,r,lf,rf)
		return result

	def SortPopulation(self):
		self.fitness = []
		for a in self.population:
			f = self.fitnessFunction(a)
			self.fitness.append(f)
		self.population = self.MergeSort(self.population,self.fitness)
		self.fitness = self.MergeSort(self.fitness,self.fitness)


	def generatePopulation(self,songs,initialSize):
		if(len(songs) == 0):
			print("No Songs!")
		for i in range(1,initialSize):
			s = songs[0:]
			child = []
			while(len(s) != 0):
				removeIndex = random.randint(0,len(s) - 1) #choose a random item
				child.append(s.pop(removeIndex))
			self.population.append(child)

	def getDataForSongs(self, songs, ENAPIKey):
		songs2 = songs[0:]
		self.songInfo = {}
		fetcher = TrackFetcher(ENAPIKey)
		for s in songs:
			info = fetcher.getInfo("spotify:track:" + s)
			if(info is not None):
				self.songInfo[s] = info
				print(info)
			else:
				print(str(s) + " not found")
				songs2.remove(s)
		self.songList = songs2


	def nextGeneration(self):
		fitness = []
		print("****")
		for mix in self.population:
			f = self.fitnessFunction(mix)
			print("Fitness: " + str(f))
			fitness.append(f)
		print("")

		b1Index = 0
		b2Index = 0

		while(b1Index == b2Index):
			b1Index = random.randint(0,(len(self.population) - 1)/2)
			b2Index = random.randint(0,(len(self.population)-1)/2)

		bestPairIndices = []
		bestPairIndices.append(b1Index)
		bestPairIndices.append(b2Index)

		self.breedPair(bestPairIndices)
		print("Best solution so far: " + str(self.population[0]))

	def breedPair(self,parentIndices):
		mix1 = self.population[parentIndices[0]]
		mix2 = self.population[parentIndices[1]]

		#generate a random mixpoint to attempt crossover from.
		mid = random.randint(1,len(mix1) - 2)

		#if the mix is small, just use the midpoint each time.
		if(mid == 0 or mid == len(mix1)-1):
			mix = len(mix1) / 2

	#mix by taking front and end of each and swapping.
		child1 = mix1[0:mid]
		child1.extend(mix2[mid:]) #might need to be mid + 1
		child2 = mix2[0:mid]
		child2.extend(mix1[mid:])

		#mutate
		if(random.randint(0,100) < 7):
			i1 = random.randint(0,len(child1) - 1)
			i2 = random.randint(0,len(child1) - 1)
			child1[i1], child2[i2] = child1[i2], child2[i1]

		
		c1Fitness = self.fitnessFunction(child1)
		c2Fitness = self.fitnessFunction(child2)
		self.insertChildIntoPopulation(child1,c1Fitness)
		self.insertChildIntoPopulation(child2,c2Fitness)

	def insertChildIntoPopulation(self,child,fitness):
		ptr = 0
		while(fitness > self.fitness[ptr] and ptr < len(self.population)):
			ptr += 1
		self.population.insert(ptr,child)
		self.fitness.insert(ptr,fitness)
		print(self.fitness) 
	def getBestMix(self):
		return self.population[0]

	#depreciated - the second one uses rms value, which works better than the cosine value.
	#Change the function used in the fitnessFunction method if you want to use this instead.
	def fitnessFunctionOne(self,mix):
		score = 0.0
		fieldsToCheck = ['danceability','energy','key','speechiness','tempo','time_signature','liveness','acousticness','mode']
		for left in range(0,len(mix) - 1):
			song1 = self.songInfo[mix[left]]
			song2 = self.songInfo[mix[left+1]]
			if(song1 is None or song2 is None):
				return 999999999.99999
			t = 0.0
			for field in fieldsToCheck:
				t += song1[field] * song2[field]

			n1 = 0.0
			for field in fieldsToCheck:
				n1 += song1[field] ** 2

			n1 = math.sqrt(n1)

			n2 = 0.0
			for field in fieldsToCheck:
				n2 += song2[field] ** 2

			n2 = math.sqrt(n2)

			if(n1 * n2 == 0):
				t = t / 0.5
			else:
				t = t / (n1 * n2)
			score += t
		return score*1000

	def fitnessFunctionTwo(self,mix):
		score = 0
		fieldsToCheck = ['danceability','energy','key','speechiness','tempo','time_signature','liveness','acousticness','mode']
		for left in range(0,len(mix) - 1):
			song1 = self.songInfo[mix[left]]
			song2 = self.songInfo[mix[left+1]]
			if(song1 is None or song2 is None):
				return 999999999.99999
			t = 0.0
			for field in fieldsToCheck:
				t += (song1[field] - song2[field]) ** 2
			score += math.sqrt(t)
		return score


	def fitnessFunction(self, mi):
		return self.fitnessFunctionTwo(mi)
