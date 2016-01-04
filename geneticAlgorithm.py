class GeneticAlgorithm(object):
	"""docstring for GeneticAlgorithm"""
	def __init__(self, initialSize,songList,ENAPIKey):
		self.population = []
		self.getDataForSongs(songList,ENAPIKey)
		self.generatePopulation(songList,initialSize)

		#tests
		# print(self.population)
		# print(self.songInfo)
		
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
		self.songInfo = {}
		fetcher = TrackFetcher(ENAPIKey)
		for s in songs:
			self.songInfo[s] = fetcher.getInfo("spotify:track:" + s)

	def nextGeneration(self):
		fitness = []
		print("****")
		for mix in self.population:
			f = self.fitnessFunction(mix)
			print("Fitness: " + str(f))
			fitness.append(f)
		print("")
		bestPairIndices = self.getTwoMinFitnessIndices(fitness)
		self.bestIndex = bestPairIndices[0]
		print("Best indices at: " + str(bestPairIndices[0]) + " and " + str(bestPairIndices[1]))
		worstPairIndices = self.getTwoMaxFitnessIndices(fitness)
		self.breedPair(bestPairIndices,worstPairIndices)
		print("Best solution so far: " + str(self.population[bestPairIndices[0]]))

	def breedPair(self,parentIndices,destinationIndices):
		mix1 = self.population[parentIndices[0]]
		mix2 = self.population[parentIndices[1]]

		#mix by taking front and end of each and swapping.
		mid = len(mix1) / 2




		child1 = mix1[0:mid]
		child1.extend(mix2[mid:]) #might need to be mid + 1
		child2 = mix2[0:mid]
		child2.extend(mix1[mid:])

		if(random.randint(0,100) < 1001):
			i1 = random.randint(0,len(child1) - 1)
			i2 = random.randint(0,len(child1) - 1)
			child1[i1], child2[i2] = child2[i2], child1[i1]

		self.population[destinationIndices[0]] = child1
		self.population[destinationIndices[1]] = child2
		print("Insert new pair at indices: " + str(destinationIndices[0]) + " and " + str(destinationIndices[1]))

	def getBestMix(self):
		return self.population[self.bestIndex]
	def getTwoMinFitnessIndices(self,fitness):
		firstMinIndex = 0
		secondMinIndex = -1
		i = 1
		while(i < len(fitness)):
			if(fitness[i] < fitness[firstMinIndex]):
				secondMinIndex = firstMinIndex
				firstMinIndex = i
			elif(fitness[i] < fitness[secondMinIndex]):
				secondMinIndex = i
			i += 1
		return [firstMinIndex,secondMinIndex]

	def getTwoMaxFitnessIndices(self,fitness):
		firstMaxIndex = 0
		secondMaxIndex = -1
		i = 1
		while(i < len(fitness)):
			if(fitness[i] > fitness[firstMaxIndex]):
				secondMaxIndex = firstMaxIndex
				firstMaxIndex = i
			elif(secondMaxIndex >= 0 and fitness[i] > fitness[secondMaxIndex]):
				secondMaxIndex = i
			i += 1
		return [firstMaxIndex,secondMaxIndex]

	def fitnessFunction(self, mix):
		score = 0.0
		fieldsToCheck = ['danceability','energy','key','speechiness','tempo','time_signature','liveness','acousticness','mode']
		for left in range(0,len(mix) - 1):
			song1 = self.songInfo[mix[left]]
			song2 = self.songInfo[mix[left+1]]

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
