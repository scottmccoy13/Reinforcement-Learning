import sys

class Map:
	def __init__(self, livReward, bridgeDanger):
		self.myMap = None #size will be set later
		self.numRows = 0
		self.numColumns = 0
		self.stateValue = {}
		self.allStates = []
		self.legalStates = []
		self.startState = None
		self.endState = None
		self.discount = 0.8
		self.livingReward = livReward
		self.bridgeDanger = bridgeDanger

	def initializeMap(self):
		with open("map.csv", "r") as mapFile:		
			num_lines = sum(1 for line in mapFile)
			mapFile.seek(0)
			line_length = len(mapFile.readline().split(","))

			self.numRows = num_lines
			self.numColumns = line_length

			#print("# rows:", num_lines)
			#print("# columns:",line_length)
			self.myMap = [["0" for x in range(line_length)] for y in range(num_lines)]

	def readMap(self):
		row = 0
		column = 0
		with open("map.csv", "r") as mapFile:
			for line in mapFile:
				line = line.rstrip()
				line = line.split(",")
				#print(line)
				for value in line:
					self.myMap[row][column] = Tile(value, self.bridgeDanger)
					if(value == 'S'):
						self.startState = (row, column)
						self.legalStates.append((row,column))
					if(value == 'F'):
						self.endState = (row, column)
						self.legalStates.append((row,column))
					if(value == 'T'):
						self.legalStates.append((row,column))
					if(value == 'B'):
						self.legalStates.append((row,column))
					column+=1
				row+=1
				column=0
		self.legalStates = list(set(self.legalStates))

	def printMap(self):
		print("Start state: ", self.startState)
		print("End state: ", self.endState)
		for i in range(self.numRows):
			for j in range(self.numColumns):
				print(self.myMap[i][j].type, end=" ")
			print('\n')

	def initializeGameState(self):
		for i in range(self.numRows):
			for j in range(self.numColumns):
				self.allStates.append((i,j))

		for key in self.allStates:
			self.stateValue[key] = 0.0
		self.stateValue["Exit"] = 100.0

	def printStateWeights(self):
		for i in range(self.numRows):
			for j in range(self.numColumns):
				print(self.stateValue[(i,j)], end=" ")
			print('\n')

	def getPossibleNextStates(self, currentPosition):
		possibleMoves = []

		#south case
		if((currentPosition[0]+1,currentPosition[1]) in self.legalStates):
			possibleMoves.append("South")
		#north case
		if((currentPosition[0]-1,currentPosition[1]) in self.legalStates):
			possibleMoves.append("North")
		#east case
		if((currentPosition[0],currentPosition[1]+1) in self.legalStates):
			possibleMoves.append("East")
		#west case
		if((currentPosition[0],currentPosition[1]-1) in self.legalStates):
			possibleMoves.append("West")

		if((currentPosition == self.endState)):
			possibleMoves = ["Exit"]

		return possibleMoves

	def getTransitionStatesAndProbs(self, state, action):
		#remember that state is a coordinate pair and
		#action is a direction
		#we should not be trying any illegal actions in 
		#this function
		if action == "South":
			if self.myMap[state[0]+1][state[1]].transitionValue == 1.0:
				prob = self.myMap[state[0]+1][state[1]].transitionValue
				return [((state[0]+1,state[1]), prob)]
			else:
				transitions = []
				prob = self.myMap[state[0]+1][state[1]].transitionValue
				transitions.append( ((state[0]+1,state[1]), prob) )
				transitions.append( (self.startState, 1-prob) )
				return transitions
		elif action == "North":
			if self.myMap[state[0]-1][state[1]].transitionValue == 1.0:
				prob = self.myMap[state[0]-1][state[1]].transitionValue
				return [((state[0]-1,state[1]), prob)]
			else:
				transitions = []
				prob = self.myMap[state[0]-1][state[1]].transitionValue
				transitions.append( ((state[0]-1,state[1]), prob) )
				transitions.append( (self.startState, 1-prob) )
				return transitions
		elif action == "East":
			if self.myMap[state[0]][state[1]+1].transitionValue == 1.0:
				prob = self.myMap[state[0]][state[1]+1].transitionValue
				return [((state[0],state[1]+1), prob)]
			else:
				transitions = []
				prob = self.myMap[state[0]][state[1]+1].transitionValue
				transitions.append( ((state[0],state[1]+1), prob) )
				transitions.append( (self.startState, 1-prob) )
				return transitions
		elif action == "West":
			if self.myMap[state[0]][state[1]-1].transitionValue == 1.0:
				prob = self.myMap[state[0]][state[1]-1].transitionValue
				return [((state[0],state[1]-1), prob)]
			else:
				transitions = []
				prob = self.myMap[state[0]][state[1]-1].transitionValue
				transitions.append( ((state[0],state[1]-1), prob) )
				transitions.append( (self.startState, 1-prob) )
				return transitions
		elif action == "Exit":
			return [("Exit",1.0)]
	
	def getReward(self, state, action, nextState):
		if(nextState == "Exit"):
			return self.livingReward + 100

		rewardOfState = self.myMap[state[0]][state[1]].reward

		return self.livingReward + rewardOfState

	def computeQValueFromValues(self, state, action):
		Qvalue = 0

		#a list of state,prob pairs
		delta = self.getTransitionStatesAndProbs(state, action)
		#print(delta)
		#input()
		sigma = 0
		for item in delta:
			if item[1] <= 0.0:
				delta.remove(item)
		for item in delta:
			reward = self.getReward(state, action, item[0])
			prob = item[1]

			sigma += reward
			sigma += (self.discount * (prob * self.stateValue[item[0]]))
			Qvalue += sigma

			sigma = 0

		return Qvalue
		
	def printMapValues(self):
		for i in range(self.numRows):
			for j in range(self.numColumns):
				print(self.stateValue[(i,j)], end=" ")
			print('\n')

	def writeMapValuesToFile(self):
		with open("output.csv", "w+") as output:
			for i in range(self.numRows):
				for j in range(self.numColumns):
					output.write( str(round(self.stateValue[(i,j)], 2)) )
					output.write(",")
				output.write('\n')

class Tile:
	def __init__(self, tileType, bridgeDanger):
		self.type = tileType
		self.reward = self.setReward()
		self.bridgeDanger = bridgeDanger
		#transition value is the probability that you will end
		#up in the state that you were intending to end in
		self.transitionValue = self.setTransitionValue()

	def setReward(self):
		if(self.type == 'W'):
			return -10.0
		elif(self.type == 'F'):
			return 0.0
		elif(self.type == 'B'):
			return 0.0
		elif(self.type == 'T'):
			return 0.0
		elif(self.type == 'S'):
			return 0.0
		else:
			print("FILE READ ERROR IN setReward()")
			exit(0)

	def setTransitionValue(self):
		if(self.type == 'W'):
			return 0.0
		elif(self.type == 'F'):
			return 1.0
		elif(self.type == 'B'):
			return self.bridgeDanger
		elif(self.type == 'T'):
			return 1.0
		elif(self.type == 'S'):
			return 1.0
		else:
			print("ERROR IN setTransitionValue()")
			exit(0)

class UserAgent:
	def __init__(self, gameMap):
		self.score = 0.0
		self.gameBoard = gameMap
		self.position = self.gameBoard.startState

	def valueIteration(self):
		Uprime = self.gameBoard.stateValue.copy()
		#print(self.gameBoard.legalStates)
		for i in range(200):
			Uprime = self.gameBoard.stateValue.copy()
			for state in self.gameBoard.legalStates:
				stateVal = None
				for action in self.gameBoard.getPossibleNextStates(state):
					currValue = self.gameBoard.computeQValueFromValues(state, action)

					if stateVal == None or stateVal < currValue:
						stateVal = currValue

				if stateVal == None:
					stateVal = 0

				Uprime[state] = stateVal

			self.gameBoard.stateValue = Uprime.copy()


if __name__ == "__main__":
	if(len(sys.argv) < 3):
		print("Invalid input form")
		print("Proper form: 'python3 map.py [living reward] [bridge danger]")
		exit(0)
	
	map = Map(float(sys.argv[1]), float(sys.argv[2]))
	map.initializeMap()
	map.readMap()
	#map.printMap()
	map.initializeGameState()
	#map.printStateWeights()

	agent = UserAgent(map)
	agent.valueIteration()

	map.printMapValues()
	map.writeMapValuesToFile()

