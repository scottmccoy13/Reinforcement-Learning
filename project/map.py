class Map:
	def __init__(self):
		self.myMap = None #size will be set later
		self.numRows = 0
		self.numColumns = 0

	def initializeMap(self):
		with open("map.csv", "r") as mapFile:		
			num_lines = sum(1 for line in mapFile)
			mapFile.seek(0)
			line_length = len(mapFile.readline().split(","))

			self.numRows = num_lines
			self.numColumns = line_length

			print("# rows:", num_lines)
			print("# columns:",line_length)
			self.myMap = [["0" for x in range(line_length)] for y in range(num_lines)]

	def readMap(self):
		row = 0
		column = 0
		with open("map.csv", "r") as mapFile:
			for line in mapFile:
				line = line.split(",")
				for value in line:
					self.myMap[row][column] = value
					column+=1
				row+=1

	def printMap(self):
		for i in range(self.numRows):
			for j in range(self.numColumns):
				print(self.myMap[i][j], end=" ")
			print('\n')



if __name__ == "__main__":
	map = Map()
	map.initializeMap()
	map.readMap()
	map.printMap()
