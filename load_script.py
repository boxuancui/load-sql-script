import os
import csv
import sys
import time
from datetime import datetime

# Variable initialization
currentDir = os.getcwd()
scriptName = sys.argv[0]
fileName = sys.argv[1]
hasHeader = sys.argv[2]
dlm = sys.argv[3]
tableName = sys.argv[4]
header = []
dataRow = []
dataInfo = []
scanLine = 0
lenCol = {}

# Read file and parse it row by row based on delimiter
if dlm == "\\t":
	file = csv.reader(open(fileName, "r"), delimiter = "\t")
else:
	file = csv.reader(open(fileName, "r"), delimiter = dlm)

# Read first line of file for later process
firstLine = file.next()
nCol = len(firstLine)
for i in range(nCol):
	lenCol[i] = 0

# Detect data type of a given element
def getType(value):
	dataTypes = [
		(int, int),
		(float, float),
		(datetime, lambda value: datetime.strptime(value, "%Y/%m/%d")),
		(datetime, lambda value: datetime.strptime(value, "%m/%d/%Y")),
		(datetime, lambda value: datetime.strptime(value, "%d/%m/%Y")),
		(datetime, lambda value: datetime.strptime(value, "%Y-%m-%d")),
		(datetime, lambda value: datetime.strptime(value, "%m-%d-%Y")),
		(datetime, lambda value: datetime.strptime(value, "%d-%m-%Y")),
		(datetime, lambda value: datetime.strptime(value, "%y/%m/%d")),
		(datetime, lambda value: datetime.strptime(value, "%m/%d/%y")),
		(datetime, lambda value: datetime.strptime(value, "%d/%m/%y")),
		(datetime, lambda value: datetime.strptime(value, "%y-%m-%d")),
		(datetime, lambda value: datetime.strptime(value, "%m-%d-%y")),
		(datetime, lambda value: datetime.strptime(value, "%d-%m-%y"))
	]
	for type, test in dataTypes:
		try:
			test(value)
			return type
		except ValueError:
			pass
	return str

# Set data type for a given element
def setType(item):
	dataDict = {}
	dataType = getType(item).__name__
	if dataType == "int":
		value = int(item)
	elif dataType == "float":
		value = float(item)
	elif dataType == "str":
		value = len(item)
	elif dataType == "datetime":
		value = item
	else:
		print "Unsupported data type detected! Currently support 'int', 'float', 'string' and 'datetime'."
	dataDict[dataType] = value
	return dataDict

# Main method
if __name__ == "__main__":
	if hasHeader.lower()[0] == "y": # If data has header, set it as first line and start scanning from next line
		header = firstLine
		dataRow = file.next()
	elif hasHeader.lower()[0] == "n": # If data does not have header, set column header and start scanning from first line
		for i in range(nCol):
			header.append("V" + str(i))
		dataRow = firstLine
	else:
		print "Please specify if the data has a header: yes or no?"

	# Scanning process starts here
	print "Start scanning ..."
	startTime = time.time()
	# Initialize data type array
	for item in dataRow:
		dataInfo.append(setType(item))
	# Loop through rows and columns to update data type array
	for row in file:
		for i in range(nCol):
			if lenCol[i] < len(row[i]):
				lenCol[i] = len(row[i])
			currentType = getType(row[i]).__name__
			if (dataInfo[i].keys()[0] != currentType) and (dataInfo[i].keys()[0] not in ("str", "datetime")):
				dataInfo[i][currentType] = dataInfo[i].pop(dataInfo[i].keys()[0])
		scanLine += 1
		if scanLine % 5000 == 0:
			print str(scanLine) + " lines scanned ..."
	# Calculate and parse elapsed time
	elapsedTime = time.time() - startTime
	if elapsedTime < 60:
		displayTime = str(round(elapsedTime, 4)) + "s"
	elif elapsedTime < 3600:
		displayTime = str(int(elapsedTime / 60)) + "m" + str(round(elapsedTime % 60, 2)) + "s"
	else:
		displayTime = str(int(elapsedTime / 3600)) + "h" + str(int(elapsedTime % 3600 / 60)) + "m" + str(round(elapsedTime % 3600 % 60, 2)) + "s"

	# Print scanning statistics to console
	print "Scanning completed! Total number of rows: " + str(scanLine)
	print "Total scanning time: " + displayTime + "."

	# Create output file
	outputFile = open("SQL_Load_Script.sql", "w")
	outputFile.write("create table " + tableName + " (\n")
	for i in range(nCol):
		if dataInfo[i].keys()[0] == "datetime":
			typeValue = "date,\n"
		elif dataInfo[i].keys()[0] == "str":
			typeValue = "varchar(" + str(lenCol[i]) + "),\n"
		elif dataInfo[i].keys()[0] == "int":
			if dataInfo[i]["int"] < 30000:
				typeValue = "smallint,\n"
			elif dataInfo[i]["int"] < 2000000000:
				typeValue = "int,\n"
			else:
				typeValue = "bigint,\n"			
		elif dataInfo[i].keys()[0] == "float":
			typeValue = "float,\n"
		else:
			print "Additional data types detected! Something is wrong."
		writeRow = header[i] + " " + typeValue
		if i == nCol - 1:
			writeRow = writeRow[:-2]			
		outputFile.write(writeRow)
	outputFile.write("\n);")
	outputFile.close()
	print "SQL_Load_Script.sql is generated at " + currentDir + "\SQL_Load_Script.sql"


